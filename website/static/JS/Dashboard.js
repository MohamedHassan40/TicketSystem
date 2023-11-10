   var data = {
  labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
  datasets: [{
    label: "Dataset #1",
    backgroundColor: "rgba(255,99,132,0.2)",
    borderColor: "rgba(255,99,132,1)",
    borderWidth: 2,
    hoverBackgroundColor: "rgba(255,99,132,0.4)",
    hoverBorderColor: "rgba(255,99,132,1)",
    data: [65, 59, 20, 81, 56, 55, 40],
  }]
};

var options = {
  maintainAspectRatio: false,
  scales: {
    y: {
      stacked: true,
      grid: {
        display: true,
        color: "rgba(255,99,132,0.2)"
      }
    },
    x: {
      grid: {
        display: false
      }
    }
  }
};




var Selectize = /** @class */ (function () {
  function Selectize() {
      this.init();
  }
  Selectize.prototype.init = function () {
      var initValue;
      $('.action-box').selectric({
          onInit: function (element) {
              initValue = $(this).val();
          },
          onChange: function (element) {
              if ($(this).val() !== initValue)
                  $(element).parents('form').submit();
          }
      });
  };
  return Selectize;
}());
var Charts = /** @class */ (function () {
  function Charts() {
      this.colors = ["#DB66AE", "#8185D6", "#89D9DF", "#E08886"];
      this.tickColor = "#757681";
      this.initRadar();
      this.initBarHorizontal();
      this.initDoughnut();
  }

  
  Charts.prototype.initRadar = function () {
      var ctxD = $('#radarChartDark'), chartData = {
          type: 'bar',
          data: {
              labels: ["Education", "Food", "Transport", "Drinks", "Other"],
              datasets: [
                  {
                      label: "2014",
                      backgroundColor: this.convertHex(this.colors[0], 20),
                      borderColor: this.colors[0],
                      borderWidth: 1,
                      pointRadius: 2,
                      data: [51, 67, 90, 31, 16],
                  },
                  {
                      label: "2015",
                      backgroundColor: this.convertHex(this.colors[1], 20),
                      borderColor: this.colors[1],
                      borderWidth: 1,
                      pointRadius: 2,
                      data: [75, 44, 19, 22, 43],
                  },
                  {
                      label: "2015",
                      backgroundColor: this.convertHex(this.colors[2], 20),
                      borderColor: this.colors[2],
                      borderWidth: 1,
                      pointRadius: 2,
                      data: [7, 14, 29, 82, 33]
                  }
              ]
          },
          options: {
              scale: {
                  pointLabels: {
                      fontColor: this.tickColor
                  },
                  ticks: {
                      display: false,
                      stepSize: 25
                  }
              },
              legend: {
                  position: "bottom",
                  labels: {
                      boxWidth: 11,
                      fontColor: this.tickColor,
                      fontSize: 11
                  }
              }
          }
      }, myDarkRadarChart = new Chart(ctxD, chartData);
  };
  Charts.prototype.initBarHorizontal = function () {
    var ctxD = $('#barChartHDark');

    // Parse the JSON data from data attributes
    var totalAppointments = JSON.parse(ctxD.attr('data-total-appointments'));
    var totalClinicVisits = JSON.parse(ctxD.attr('data-total-clinic-visits'));
    var totalWalkinAppointments = JSON.parse(ctxD.attr('data-total-walkin-appointments'));

    var chartData = {
        type: 'horizontalBar',
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            datasets: [
                {
                    label: 'Total Appointments',
                    data: totalAppointments,
                    backgroundColor: this.colors[0],
                    hoverBackgroundColor: this.convertHex(this.colors[0], 70),
                },
                {
                    label: 'Total Clinic Visits',
                    data: totalClinicVisits,
                    backgroundColor: this.colors[1],
                    hoverBackgroundColor: this.convertHex(this.colors[1], 70),
                },
                {
                    label: 'Total Walkin Appointments',
                    data: totalWalkinAppointments,
                    backgroundColor: this.colors[2],
                    hoverBackgroundColor: this.convertHex(this.colors[2], 70),
                },
            ],
        },
        options: {
            barThickness: 10,
            scales: {
                xAxes: [{
                    stacked: true,
                    ticks: {
                        fontColor: this.tickColor,
                    },
                    gridLines: {
                        drawOnChartArea: false,
                    },
                }],
                yAxes: [{
                    stacked: true,
                    ticks: {
                        fontColor: this.tickColor,
                        min: 0,
                        max: 200, // Adjust the max value as needed
                        stepSize: 25,
                    },
                }],
            },
            legend: {
                display: true,
                labels: {
                    fontColor: this.tickColor,
                },
            },
        },
    };

    var myHorizontalBarChart = new Chart(ctxD, chartData);
};

  
  Charts.prototype.initDoughnut = function () {
    var totalEmptyRooms = parseInt(document.getElementById('doughnutChartDark').getAttribute('data-total-empty-rooms'));
    var totalOccupiedRooms = parseInt(document.getElementById('doughnutChartDark').getAttribute('data-total-occupied-rooms'));
    var totalSpaceRooms = parseInt(document.getElementById('doughnutChartDark').getAttribute('data-total-space-rooms'));
      var ctxD = $('#doughnutChartDark'), chartData = {
          type: 'doughnut',
          data: {
            labels: ["Total Empty Rooms", "Total Occupied Rooms", "Total Space Rooms"],
              datasets: [{
                data: [totalEmptyRooms, totalOccupiedRooms, totalSpaceRooms],
                      borderWidth: 0,
                      backgroundColor: [
                          this.convertHex(this.colors[0], 60),
                          this.convertHex(this.colors[1], 60),
                          this.convertHex(this.colors[2], 60),
                      ],
                      hoverBackgroundColor: [
                          this.colors[0],
                          this.colors[1],
                          this.colors[2],
                      ]
                  }]
          },
          options: {
              responsive: true,
              legend: {
                  position: "bottom",
                  labels: {
                      boxWidth: 11,
                      fontColor: this.tickColor,
                      fontSize: 11
                  }
              }
          }
      }, myDarkRadarChart = new Chart(ctxD, chartData);
  };





  Charts.prototype.convertHex = function (hex, opacity) {
      hex = hex.replace('#', '');
      var r = parseInt(hex.substring(0, 2), 16);
      var g = parseInt(hex.substring(2, 4), 16);
      var b = parseInt(hex.substring(4, 6), 16);
      var result = 'rgba(' + r + ',' + g + ',' + b + ',' + opacity / 100 + ')';
      return result;
  };
  return Charts;
}());
new Selectize();
new Charts();

$(function() {
  // Owl Carousel
  var owl = $(".owl-carousel");
  owl.owlCarousel({
    items: 4,
    margin: 10,
    loop: true,
    autoplay: true,
    nav: true
  });
});



document.addEventListener("DOMContentLoaded", function () {
    // Get the canvas element
    const canvas = document.getElementById("lineChartComplaints");
    const monthlyComplaintsData = JSON.parse(canvas.getAttribute("data-monthly-complaints"));

    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

    // Get the canvas context
    const ctx = canvas.getContext("2d");

    // Create the complaints chart
    new Chart(ctx, {
        type: "line",
        data: {
            labels: months,
            datasets: [{
                label: "Number of Complaints",
                borderColor: "rgba(255, 99, 132, 1)",
                backgroundColor: "rgba(255, 99, 132, 0.2)",
                borderWidth: 2,
                hoverBackgroundColor: "rgba(255, 99, 132, 0.4)",
                hoverBorderColor: "rgba(255, 99, 132, 1)",
                data: monthlyComplaintsData,
            }],
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    grid: {
                        display: false,
                    },
                },
                y: {
                    stacked: true,
                    grid: {
                        display: true,
                        color: "rgba(255, 99, 132, 0.2)",
                    },
                },
            },
        },
    });
});































document.addEventListener("DOMContentLoaded", function () {
    // Extract department names and employee counts from the data
    var departmentNames = departmentEmployeesData.map(function (item) {
        return item.department_name;
    });

    var employeeCounts = departmentEmployeesData.map(function (item) {
        return item.employee_count;
    });

    // Create a bar chart
    var ctx = document.getElementById('departmentEmployeesChart').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: departmentNames,
            datasets: [{
                label: 'Number of Employees',
                data: employeeCounts,
                backgroundColor: 'rgba(75, 192, 192, 0.6)', // Adjust the color as needed
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Employees'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Department'
                    }
                }
            }
        }
    });
});
