import './MyChart.css';
import React from 'react';
import { Line } from 'react-chartjs-2';

const MyChart = (props) => {
  const data = {
    labels: props.execution_time.map(time => time.toFixed(2)), // Assuming execution_time is in seconds
    datasets: [
      {
        label: 'Temperature (Degrees Celsius)',
        data: props.temperatureArray,
        fill: false,
        backgroundColor: 'rgb(54, 162, 235)',
        borderColor: 'rgba(54, 162, 235, 0.2)',
      },
    ],
  };

  const options = {
    scales: {
      yAxes: [
        {
          ticks: {
            beginAtZero: true,
          },
        },
      ],
      xAxes: [
        {
          scaleLabel: {
            display: true,
            labelString: 'Time (Seconds)'
          }
        }
      ]
    },
    title: {
      display: true,
      text: 'Temperature vs. Time-Phase Change Graph',
    },
    maintainAspectRatio: false,
  };

  return <Line data={data} options={options} />;
};


export default MyChart;