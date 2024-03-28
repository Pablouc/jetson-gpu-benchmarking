import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import './ConsoleView.css';

const ConsoleView = (props) => {
  const [consoleLogs, setConsoleLogs] = useState([]);

  useEffect(() => {
    const socket = io(props.ngrokURL, {
      path: '/socket.io/', // Default path for Socket.IO
      transports: ['websocket'] // Force WebSocket transport
    });

    socket.on('connect', () => {
      console.log('Connected to WebSocket server');
      socket.emit('message', 'Hello from React');
    });

    socket.on('connect_error', (error) => {
      console.error('Connection Error:', error);
    });

    socket.on('response', (data) => {
      console.log('Received response:', data);
      // Update the consoleLogs state with the received logs
      const newConsoleLogs = Object.values(data.console_logs || {});
      setConsoleLogs(newConsoleLogs);

    });

    return () => {
      socket.disconnect();
    };
  }, [props.ngrokURL]);

  return (
    <div>
      <div className="console-label">Console Logs</div>
      <div className="scrollable-block-container">
        <div className="scrollable-block">
        {consoleLogs.map((log, index) => (
          <>
            {log.split('\n').map((line, lineIndex) => (
              <p key={`${index}-${lineIndex}`}>{line}</p>
            ))}
            {index < consoleLogs.length - 1 && (
              <>
                <br />
                <br />
              </>
            )}
          </>
        ))}
        </div>
      </div>
    </div>
  );
};

export default ConsoleView;
