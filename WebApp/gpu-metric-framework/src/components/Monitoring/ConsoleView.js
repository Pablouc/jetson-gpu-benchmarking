import React, { useEffect, useState } from 'react';
import './ConsoleView.css';

const ConsoleView = (props) => {

  return (
    <div>
      <div className="console-label">Console Logs</div>
      <div className="scrollable-block-container">
        <div className="scrollable-block">
        {props.consoleLogs.map((log, index) => (
          <>
            {log.split('\n').map((line, lineIndex) => (
              <p key={`${index}-${lineIndex}`}>{line}</p>
            ))}
            {index < props.consoleLogs.length - 1 && (
              <>
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
