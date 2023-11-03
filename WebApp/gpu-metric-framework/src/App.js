import MainView from "./components/MainView/MainView";

const ngrokURL = 'https://7e23-141-3-72-67.ngrok-free.app/';

const cfd_workloadsNamesURL = ngrokURL + 'cfd_workloads';
const bfs_workloadsNamesURL = ngrokURL + 'bfs_workloads';
const requestExecutionURL = ngrokURL + 'setExecutionRequest';
const frequenciesOptionsURL = ngrokURL + 'frequencies';
const resultsFileDataURL = ngrokURL + 'get-csv';
const currentAppsExcURL = ngrokURL + 'getCurrentApps';
const gpuDataURL = ngrokURL + 'gpu_data';
const gpuIterationsDataURL = ngrokURL + 'gpu_iterations_data';


function App() {
  return (
    <div>
      <MainView cfd_workloadsURL={cfd_workloadsNamesURL} bfs_workloadsURL={bfs_workloadsNamesURL} 
                      executionURL={requestExecutionURL} frequenciesURL={frequenciesOptionsURL} 
                      resultsFileURL={resultsFileDataURL} currentAppsURL={currentAppsExcURL}
                      gpu_dataURL={gpuDataURL} gpu_IterDataURL={gpuIterationsDataURL}/>
    </div>
  );
}

export default App;
