import React from 'react';
import { Bar } from 'react-chartjs-2';
import 'chart.js/auto';
import './Chart.css';

function MyChart(props) {
  const chartData = {
    labels: props.temperatureArray,  // These are temperatures.
    datasets: [
      {
        label: 'Power',
        data: props.powerArray, // This should match power consumption at those temperatures.
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
        fill: true,
      }
    ],
  };

  const options = {
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Temperature (°C)', // Change to your preferred unit or label
          font: {
            size: 16,
          }
        }
      }
    }
  };

  return (
    <div className='chartWrapper'>
      <div className='chartContainer'>
      <Bar data={chartData} options={options} />
      </div>
    </div>
    
  );
}

export default MyChart;
