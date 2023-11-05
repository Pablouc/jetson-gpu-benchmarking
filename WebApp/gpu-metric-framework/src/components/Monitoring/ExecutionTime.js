import React, { useState, useEffect } from 'react';
import { NativeEventSource, EventSourcePolyfill } from 'eventsource-polyfill';

// Use NativeEventSource if available; otherwise, use EventSourcePolyfill
const EventSource = NativeEventSource || EventSourcePolyfill;

function ExecutionTime(props) {
  const [executionTime, setExecutionTime] = useState('No data yet');

  useEffect(() => {
    let eventSource;

    // Function to initialize the SSE connection
    const initializeSSE = () => {
      eventSource = new EventSource(props.execTimeURL, {
        headers: {
          'ngrok-skip-browser-warning': '1'
        }
      });

      eventSource.onmessage = (event) => {
        console.log('New execution time:', event.data);
        setExecutionTime(event.data);
      };

      eventSource.onerror = (error) => {
        console.error('EventSource failed:', error);
        eventSource.close(); // Close the connection on error

        // Attempt to reconnect after 5 seconds
        setTimeout(() => {
          console.warn('Reconnecting...');
          initializeSSE();
        }, 5000);
      };
    };

    // Initialize the SSE connection when the component mounts
    initializeSSE();

    // Clean up before the component unmounts
    return () => {
      if (eventSource) {
        console.log('Closing EventSource');
        eventSource.close();
      }
    };
  // If props.execTimeURL is stable, you can omit it from the dependencies array
  // Otherwise, if it changes, it should be included so that the effect reruns with the new URL
  }, [props.execTimeURL]); 

  return (
    <div className="App">
      <header className="App-header">
        <p>Execution Time: {executionTime}</p>
      </header>
    </div>
  );
}

export default ExecutionTime;
