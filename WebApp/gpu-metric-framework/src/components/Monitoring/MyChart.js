import React from 'react';
import { Chart, Line } from 'react-chartjs-2';
import 'chart.js/auto';
import './MyChart.css';

const MyChart = (props) => {
  // Assuming the temperature values are centered around 40, calculate min and max
  let max_yAxis_value = 0;
  let min_yAxis_value = 0;
  let yAxis_Array=[];
  if (props.label[0] == 'Temperature'){
    max_yAxis_value = Math.max(...props.temperatureArray);
    min_yAxis_value = Math.min(...props.temperatureArray);
    yAxis_Array = props.temperatureArray;
  }

  if (props.label[0] == 'Power'){
    max_yAxis_value = Math.max(...props.powerArray);
    min_yAxis_value = Math.min(...props.powerArray);
    yAxis_Array = props.powerArray;
  }

  
  

  const data = {
    labels: props.execution_time.map(time => time.toFixed(2)),
    datasets: [
      {
        label: props.label[0],
        data: yAxis_Array,
        fill: false,
        borderColor: 'blue',
        tension: 0.1,
        pointRadius: 3,
      }
    ]
  };

  const options = {
    scales: {
      y: {
        beginAtZero: false,
        suggestedMin: min_yAxis_value - 1, // slightly lower than the minimum data value
        suggestedMax: max_yAxis_value + 1, // slightly higher than the maximum data value
        ticks: {
          // Include the degree sign and fine-tune the step size
          stepSize: 1 // Adjust step size to control how many ticks are shown
        },
        title: { // This is where you set the Y axis title
          display: true,
          text: props.label[1]
        }
      },
      x: {
        ticks: {
          autoSkip: true,
          maxTicksLimit: 20 // Adjust based on your data
        },
        title: { // This is where you set the X axis title
          display: true,
          text: 'Execution Time (s)'
        }
      }
    },
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: props.label[0] + ' vs Execution Time',
      }
    },
  };

  return (
    <div className="chartContainer">
      <Line data={data} options={options} />
    </div>
  );
};

export default MyChart;
