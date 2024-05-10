import React, { useState, useEffect  } from 'react';
import DynamicCheckbox from '../Request-Execution/DynamicCheckbox';
import './AppComponents.css';
import Dropdown from '../Request-Execution/Dropdown';

const AppComponent = (props) => {
  
    let userData={}

    const [isChecked, setIsChecked] = useState(false);

    //Constants to save inputs values
    const [cfd_threads, set_cfd_Threads] = useState('');
    const [niter, setNiter] = useState('');
    const [lambda, setLambda] = useState('');
    const [nc, setNc] = useState('');
    const [nr, setNr] = useState('');
    const [iterations, setiterations] = useState('');
    const [freq_min, setfreq_min] = useState('');
    const [freq_max, setfreq_max] = useState('');
    const [delay, setdelay] = useState('');
    const [matrixSize, setMatrixSize] = useState('');
    const [lud_threads, set_lud_threads] = useState('');
    const [boxes, setBoxes] = useState('');
    const [externalName, setExternalName] = useState('');
    const [externalWorkload, setExternalWorkload] = useState('');
    const [make_isChecked, setMakeIsChecked] = useState(false);
    const [make_input, setMakeInput] = useState('');
    const [power, setPower] = useState('');

    const executeHandler = ( enteredUserData ) => {
        userData = {
            ...userData, // Keep the existing data in userData
            ...enteredUserData, // Add the data from enteredUserData
        };
        if (props.appName == 'Gauss'){
            const gaussApp={
                gauss_name: 'Gauss',
                gauss_workloads : userData.gauss_workload
            }
            props.onExecuteEvent(gaussApp);
        }
        if (props.appName == 'BFS'){
            const bfs = {
                bfs_name:'BFS',
                bfs_workloads : userData.bfs_workload
            }
            props.onExecuteEvent(bfs);
        }

        if(props.appName == 'Wicked'){
            if(userData.wicked_minfreq != undefined){
                setfreq_min(userData.wicked_minfreq);
            }
            if(userData.wicked_maxfreq != undefined){
                setfreq_max(userData.wicked_maxfreq);
            }
        }
    }

    const handle_makeCheckbox = () => {
        setMakeIsChecked(prevState => !prevState); 
    };

    const handleCheckboxChange = () => {
        setIsChecked(prevState => !prevState); 
    };


    const handleRadioChange = (event) => {
        setPower(event.target.value);
    };

    //Sending data the the parent
    useEffect(() => {
    // This code will run after the state has been updated
    if( props.refresh == true){
        setIsChecked(false);
        set_cfd_Threads('');
        setNiter('');
        setLambda('');
        setNc('');
        setNr('');
        setiterations('');
        setfreq_min('');
        setfreq_max('');
        setdelay('');
        setMatrixSize('');
        set_lud_threads('');
        setBoxes('');
        setExternalName('');
        setExternalWorkload('');
        setMakeIsChecked(false);
        setMakeInput('');
    }

    /*if(props.appName=='Gauss'){
        const cfd={ 
        gauss_name: 'Gauss'
        };
        if(gauss_threads!='') props.onExecuteEvent(cfd); 
    } */

    else if(props.appName=='LavaMD'){
        const lavaMD={ 
        lava_name: 'LavaMD',
        lava_workloads:' -boxes1d '+ boxes
        };

        if(boxes!='') props.onExecuteEvent(lavaMD); 
    }

    else if(props.appName=='Wicked'){
        const wicked={ 
        wicked_name: 'Wicked',
        wicked_workloads: ' '  +  String(freq_min) + ' ' + String(freq_max) + ' ' + String(delay) + ' ' + String(power)
        };
        if((freq_min!='') && (freq_max!='') && (delay!='') && (power!='')) props.onExecuteEvent(wicked); 
    }

    else if(props.appName=='Srad'){
        const srad={ 
        srad_name: 'Srad',
        srad_workloads: String(niter) + ' ' + String(lambda) + ' ' +  String(nr)+ ' ' + String(nc)
        };
        if((niter!='') && (lambda!='') && (nr!='') && (nc!='')) props.onExecuteEvent(srad); 
    }

    else if(props.appName=='Lud'){
        const lud={ 
        lud_name: 'Lud',
        lud_workloads: ' -s ' + matrixSize ,
        lud_threads: lud_threads
        };
        if((matrixSize!='') && (lud_threads!='')) props.onExecuteEvent(lud); 
    }
    
    else if(props.appName=='External'){
        const external_app={ 
        appName: externalName,
        workload_input: externalWorkload,
        makefile_flag: make_isChecked,
        makefile_input : make_input
        };
        if((externalName!='') && (externalWorkload!='')) props.onExecuteEvent(external_app); 
    } 
    }, [props.refresh ,userData, cfd_threads, niter, lambda, nc, nr, iterations, freq_min, freq_max, delay,
         matrixSize, lud_threads, boxes, externalName, externalWorkload]);
    


  return (
    <div className='app-style'>
      <label>
      <input type="checkbox" checked={isChecked} onChange={handleCheckboxChange}/>{props.appName}
      </label>
      <div className='text-style'>
        
        { isChecked && (props.appName == 'BFS') && (
            <>
            <label>Workloads files:</label>
            <DynamicCheckbox itemsURL={props.itemsURL} appName={'BFS'} onExecuteEvent = {executeHandler}/>
            </>
        )}

        { isChecked && (props.appName == 'Gauss') && (
        <>
            <label>Workloads files:</label>
            <DynamicCheckbox itemsURL={props.itemsURL} appName={'Gauss'} onExecuteEvent = {executeHandler}/>
            
        </>
        )}

        {isChecked && (props.appName == 'LavaMD') && (
        <>
            <div>
                <label>Number of boxes</label>
                <input type='number' className='input-style' value={boxes} onChange={e => setBoxes(e.target.value)}></input>
            </div>
        </>
        )}

        {isChecked && (props.appName == 'Wicked') && (
            <>

                <div>
                    <label >Select min frequency (MHz)</label>
                    <Dropdown refresh={props.refresh} injected={true} wickedApp={true} freq_boundary={'min'} frequenciesURL={props.frequenciesURL} onExecuteEvent = {executeHandler}></Dropdown>
                </div>

                {/* <div>
                    <label>freq_min</label>
                    <input type='number' className='input-style' value={freq_min} onChange={e => setfreq_min(e.target.value)}></input>
                </div> */}

                <div>
                    <label >Select min frequency (MHz)</label>
                    <Dropdown refresh={props.refresh} injected={true} wickedApp={true} freq_boundary={'max'} frequenciesURL={props.frequenciesURL} onExecuteEvent = {executeHandler}></Dropdown>
                </div>

               {/*  <div>
                    <label>Number of frames</label>
                    <input type='number' className='input-style' value={freq_max} onChange={e => setfreq_max(e.target.value)}></input>
                </div> */}

                <div>
                    <label>Delay</label>
                    <input type='number' className='input-style' value={delay} onChange={e => setdelay(e.target.value)}></input>
                </div>

                <div>
                    <label>Power mode(W)</label>
                    <input type='radio' name='power' class='input-style' value='10' checked={power === '10'} onChange={handleRadioChange}/>10W
                    <input type='radio' name='power' class='input-style' value='5' checked={power === '5'} onChange={handleRadioChange}/>5W
                </div>
            </>
        )}

        {isChecked && (props.appName == 'Srad') && (
            <>
                <div>
                    <label>Algorithm iterations in the image</label>
                    <input type='number' className='input-style' value={niter} onChange={e => setNiter(e.target.value)}></input>
                </div>

                <div>
                    <label>Amount of diffusion</label>
                    <input type='number' step="0.01" className='input-style' value={lambda} onChange={e => setLambda(e.target.value)}></input>
                </div>

                <div>
                    <label>Number of rows</label>
                    <input type='number' className='input-style' value={nr} onChange={e => setNr(e.target.value)}></input>
                </div>

                <div>
                    <label>Number of columns</label>
                    <input type='number' className='input-style' value={nc} onChange={e => setNc(e.target.value)}></input>
                </div>
            </>
        )}




        {isChecked && (props.appName == 'Lud') && (
            <>
                <div>
                    <label>Matrix size</label>
                    <input type='number' className='input-style' value={matrixSize} onChange={e => setMatrixSize(e.target.value)}></input>
                </div>

                <div>
                    <label>Threads per block</label>
                    <input type='number' className='input-style' value={lud_threads} onChange={e => set_lud_threads(e.target.value)}></input>
                </div>
            </>
        )}

        {isChecked && (props.appName == 'External') && (
            <>
                <div>
                    <label>Application name</label>
                    <input type='text' className='input-style' value={externalName} onChange={e => setExternalName(e.target.value)}></input>
                </div>

                <div>
                    <label>Workload input</label>
                    <input type='text' className='input-style' value={externalWorkload} onChange={e => setExternalWorkload(e.target.value)}></input>
                </div>

                <div className='input-style'>
                    <label>
                    <input type="checkbox" checked={make_isChecked} onChange={handle_makeCheckbox}/>Does it require compilation?
                    </label>
                </div>

                <div>
                    {make_isChecked && (
                    <>
                        <label>Makefile input</label>
                        <input type='text' className='input-style' value={make_input} onChange={e => setMakeInput(e.target.value)}></input>
                    </>
                    )}
                </div>
            </>
            )}
      </div>
      
      
    </div>
  );
};

export default AppComponent;
