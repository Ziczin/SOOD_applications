// build-esbuild.js
// Minimal esbuild bundler for this project. Place this file in project root (next to make.js).
// It will bundle `ENTRY` (default: ./make.js) into OUT_DIR and write manifest.json.
// You can replace this with your own build script — this placeholder will only be created if missing.

const esbuild = require('esbuild');
const fs = require('fs');
const path = require('path');

const ENTRY = process.env.ENTRY || path.resolve(__dirname, 'make.js'); // override with env var
const OUT_DIR = process.env.OUT_DIR || path.resolve(__dirname, 'static', 'collected');

(async () => {
  try {
    if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });
    const tmpOut = path.join(OUT_DIR, 'static.tmp.js');
    const result = await esbuild.build({
      entryPoints: [ENTRY],
      bundle: true,
      minify: true,
      sourcemap: false,
      metafile: true,
      splitting: false,
      format: 'iife',
      globalName: 'AppBundle',
      platform: 'browser',
      target: ['es2018'],
      outfile: tmpOut,
    });

    // move/rename js to fixed name (no hash)
    const finalName = `static.js`;
    const finalPath = path.join(OUT_DIR, finalName);
    if (fs.existsSync(finalPath)) fs.unlinkSync(finalPath);
    fs.renameSync(tmpOut, finalPath);

    // handle css output (if any) - fixed name static.css
    let cssFinal = null;
    const cssOutputs = Object.keys(result.metafile.outputs || {}).filter(p => p.endsWith('.css'));
    if (cssOutputs.length) {
      const cssPath = path.resolve(cssOutputs[0]);
      if (fs.existsSync(cssPath)) {
        const cssName = `static.css`;
        const cssFinalPath = path.join(OUT_DIR, cssName);
        if (fs.existsSync(cssFinalPath)) fs.unlinkSync(cssFinalPath);
        fs.renameSync(cssPath, cssFinalPath);
        cssFinal = cssName;
      }
    }

    const manifest = {
      "static.js": path.relative(process.cwd(), finalPath).replace(/\\/g, '/')
    };
    if (cssFinal) manifest['static.css'] = path.relative(process.cwd(), path.join(OUT_DIR, cssFinal)).replace(/\\/g, '/');

    fs.writeFileSync(path.join(OUT_DIR, 'manifest.json'), JSON.stringify(manifest, null, 2), 'utf8');
  } catch (e) {
    console.error('Build failed', e);
    process.exit(1);
  }
})();
