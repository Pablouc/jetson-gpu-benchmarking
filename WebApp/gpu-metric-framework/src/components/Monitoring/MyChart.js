import React, { useRef } from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { Line } from 'react-chartjs-2';
import './MyChart.css';
import image from '../../Images/download-icon.png';

// Register the components required by ChartJS to draw the line chart
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const MyChart = (props) => {
  const chartRef = useRef(null); // Define the chartRef

  // Updated function to download the chart as an image
  const downloadChart = () => {
    const canvas = chartRef.current.canvas; // Assuming chartRef is attached to the canvas element

    canvas.toBlob(function(blob) {
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${props.label[0]}_chart.png`; // Dynamic filename based on chart label
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link); // Remove the link when done
      URL.revokeObjectURL(url); // Free up memory by releasing object URL
    }, 'image/png');
  };
  let max_yAxis_value = 0;
  let min_yAxis_value = 0;
  let yAxis_Array = [];

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

  if (props.label[0] == 'RAM'){
    max_yAxis_value = Math.max(...props.ramArray);
    min_yAxis_value = Math.min(...props.ramArray);
    yAxis_Array = props.ramArray;
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
    <div >
      <div className='button-cont'>
        <button onClick={downloadChart}  style={{ padding: 0, border: 'none' }}>
          <img src={image} alt="Button Image" className='button-image'/>
          </button>
      </div>
      <div className="chartContainer">
        <Line ref={chartRef} data={data} options={options} />
      </div>
      
    </div>
  );
};

export default MyChart;
