import preferences from './preferences.js'

export default {
    preferences,
    
    all: (group_name, tests, detailed = false) => {
        let passed = 0;
        let total = 0;
        console.log(`Testing ${group_name}:`);
        for (const [rawName, testFn] of Object.entries(tests)) {
            let testName = rawName
                .replace(/^test/i, '')
                .replace(/([A-Z])/g, ' $1')
                .replace(/_/g, ' ')
                .trim()
                .toLowerCase()
                .replace(/^\w/, c => c.toUpperCase());
            total++;
            try {
                const result = testFn();
                if (result) {
                    passed++;
                    if (detailed) {
                        console.log(`✅ - ${testName}`);
                    }
                } else {
                    if (detailed) {
                        console.log(`❌ - ${testName}`);
                    }
                }
            } catch (error) {
                if (detailed) {
                    console.log(`❗ ${testName} ERROR: ${error.message}`);
                }
            }
        }

        const percentage = Math.round((passed / total) * 100);
        let emoji;
        if (percentage === 100) { emoji = '✅'; }
        else if (percentage >= 90) { emoji = '⚠️'; }
        else if (percentage >= 50) { emoji = '❌'; }

        console.log(`Passed: ${passed}/${total} ${emoji} (${percentage}%)`);
        return { passed, total, percentage };
    }
}