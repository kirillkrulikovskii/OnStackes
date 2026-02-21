// Loop that prints timestamps every second for 5 iterations
let count = 0;
const maxIterations = 6000;


const intervalId = setInterval(() => {
    // Current timestamp in milliseconds
    const timestampMs = Date.now();

    // Human-readable ISO timestamp
    const timestampISO = new Date().toISOString();

    console.log(`Iteration ${count + 1}:`);
    console.log(`  Milliseconds: ${timestampMs}`);
    console.log(`  ISO Format  : ${timestampISO}`);
    console.log('-----------------------------');
    
    document.getElementById('timestamp').innerHTML = timestampISO;
    

    count++;

    // Stop after maxIterations
    if (count >= maxIterations) {
        clearInterval(intervalId);
        console.log("Loop finished.");
    }
}, 1000); // 1000 ms = 1 second
