function choose_particles_config() {
  let base_path = "particles/";
  let config = base_path + "default.json";

  let date = new Date();
  let month = date.getMonth();
  let day = date.getDate();

  // Spring
  if (1 < month && month < 5) {
    // config = base_path + "spring.json"
  }
  // Summer
  if (4 < month && month < 5) {
    // config = base_path + "summer.json"
  }
  // Autumn
  if (7 < month && month < 10) {
    config = base_path + "autumn.json";
  }
  // Winter
  else if (month > 9 || month < 2) {
    config = base_path + "winter.json";
    // Halloween
    if (month == 9 && day == 31) {
    }
    // Bonfire night
    if (month == 10 && day == 5) {
    }
    // Christmas
    if (month == 11 && day == 25) {
      // config = base_path + "xmas.json"
    }
    // New Year
    if ((month == 11 && day == 31) || (month == 0 && day == 1)) {
      config = base_path + "new-year.json";
    }
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
