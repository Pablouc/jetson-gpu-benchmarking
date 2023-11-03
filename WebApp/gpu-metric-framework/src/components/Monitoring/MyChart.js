import React from 'react';
import { Bar } from 'react-chartjs-2';
import 'chart.js/auto';
import './MyChart.css';

function MyChart(props) {
  const chartData = {
    labels: props.temperatureArray,  // These are temperatures.
    datasets: [
      {
        label: 'Temperature (°C)',
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
          text: 'Power (W)', // Change to your preferred unit or label
          font: {
            size: 16,
          }
        }
      }
    },
    plugins: {
      tooltip: {
        callbacks: {
          title: function(tooltipItem, data) {
            // This will show the correct power value as the title
            return 'Power: ' + tooltipItem[0].formattedValue + ' W';
          },
          label: function(tooltipItem, data) {
            // This will show the correct temperature value as the label
            return 'Temperature: ' + tooltipItem.chart.data.labels[tooltipItem.dataIndex] + ' °C';
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