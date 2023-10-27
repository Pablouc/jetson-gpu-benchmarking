//import React, { useState } from 'react';
import './Popup.css';

const Popup = ({ isOpen, onClose }) => {
  if (!isOpen) {
    return null;
  }

  return (
    <div >
      <div >
        {/* Your popup content goes here */}
        <h2>Successful Execution</h2>
        <label className='label-style'>Click here to access monitoring view</label>
        <div>
            <button className='popup-button' onClick={onClose}>Open</button>
        </div>
        
      </div>
    </div>
  );
};

export default Popup;