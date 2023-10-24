const { exec } = require('child_process');
function updateVelocity() {
  // Run the Python script
  exec('python motor_velocity.py', (error, stdout, stderr) => {
    if(stdout){
      // Update the HTML element with the current velocity
      document.querySelector(".text-wrapper-4").textContent = stdout;
    }
    if (stderr) {
      console.error(`stderr: ${stderr}`);
    }
    if (error) {
      console.error(`Error: ${error}`);
    }
  });
};

export default updateVelocity;