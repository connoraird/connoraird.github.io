function choose_particles_config() {
  let base_path = "particles/";
  let config = base_path + "default.json";

  let date = new Date();
  let month = date.getMonth();
  let day = date.getDate();

  // Winter in December
  if (month == 11) {
    config = base_path + "winter.json";
  }
  // New Year
  if ((month == 11 && day == 31) || (month == 0 && day == 1)) {
    config = base_path + "new-year.json";
  }

  return config;
}

document.addEventListener("DOMContentLoaded", function () {
  let config_file = choose_particles_config();

  tsParticles
    .loadJSON("tsparticles", config_file)
    .then((container) => {
      console.log("callback - tsparticles config loaded");
    })
    .catch((error) => {
      console.error(error);
    });
});
