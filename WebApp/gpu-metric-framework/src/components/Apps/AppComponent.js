import React, { useState, useEffect  } from 'react';
import DynamicCheckbox from '../Request-Execution/DynamicCheckbox';
import './AppComponents.css';

const AppComponent = (props) => {
  
    let userData={}

    const [isChecked, setIsChecked] = useState(false);

    //Constants to save inputs values
    const [cfd_threads, set_cfd_Threads] = useState('');
    const [niter, setNiter] = useState('');
    const [lambda, setLambda] = useState('');
    const [nc, setNc] = useState('');
    const [nr, setNr] = useState('');
    const [width, setWidth] = useState('');
    const [height, setHeight] = useState('');
    const [nfr, setNfr] = useState('');
    const [np, setNp] = useState('');
    const [matrixSize, setMatrixSize] = useState('');
    const [lud_threads, set_lud_threads] = useState('');
    const [boxes, setBoxes] = useState('');
    const [externalName, setExternalName] = useState('');
    const [externalWorkload, setExternalWorkload] = useState('');
    const [make_isChecked, setMakeIsChecked] = useState(false);
    const [make_input, setMakeInput] = useState('');

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
        else if (props.appName == 'BFS'){
            const bfs = {
                bfs_name:'BFS',
                bfs_workloads : userData.bfs_workload
            }
            props.onExecuteEvent(bfs);
        }
    }

    const handle_makeCheckbox = () => {
        setMakeIsChecked(prevState => !prevState); 
    };

    const handleCheckboxChange = () => {
        setIsChecked(prevState => !prevState); 
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
        setWidth('');
        setHeight('');
        setNfr('');
        setNp('');
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

    else if(props.appName=='Particle Filter'){
        const particle={ 
        filter_name: 'Particle Filter',
        filter_workloads: ' -x ' + width + ' -y ' + height + ' -z ' + nfr + ' -np ' + np
        };
        if((width!='') && (height!='') && (nfr!='') && (np!='')) props.onExecuteEvent(particle); 
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
    }, [props.refresh ,userData, cfd_threads, niter, lambda, nc, nr, width, height, nfr, np,
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

        {isChecked && (props.appName == 'Particle Filter') && (
            <>
                <div>
                    <label>Width</label>
                    <input type='number' className='input-style' value={width} onChange={e => setWidth(e.target.value)}></input>
                </div>

                <div>
                    <label>Height</label>
                    <input type='number' className='input-style' value={height} onChange={e => setHeight(e.target.value)}></input>
                </div>

                <div>
                    <label>Number of frames</label>
                    <input type='number' className='input-style' value={nfr} onChange={e => setNfr(e.target.value)}></input>
                </div>

                <div>
                    <label>Number of particles</label>
                    <input type='number' className='input-style' value={np} onChange={e => setNp(e.target.value)}></input>
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
                    <input type="checkbox" checked={make_isChecked} onChange={handle_makeCheckbox}/>Does it require execution of the makefile?
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
