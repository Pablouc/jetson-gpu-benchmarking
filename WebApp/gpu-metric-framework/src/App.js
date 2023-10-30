import MainView from "./components/MainView/MainView";

const ngrokURL = 'https://f10c-141-3-72-67.ngrok-free.app/';

const cfd_workloadsNamesURL = ngrokURL + 'cfd_workloads';
const bfs_workloadsNamesURL = ngrokURL + 'bfs_workloads';
const requestExecutionURL = ngrokURL + 'setExecutionRequest';
const frequenciesOptionsURL = ngrokURL + 'frequencies';
const resultsFileDataURL = ngrokURL + 'get-csv';
const currentAppsExcURL = ngrokURL + 'getCurrentApps';


function App() {
  return (
    <div>
      <MainView cfd_workloadsURL={cfd_workloadsNamesURL} bfs_workloadsURL={bfs_workloadsNamesURL} 
                      executionURL={requestExecutionURL} frequenciesURL={frequenciesOptionsURL} 
                      resultsFileURL={resultsFileDataURL} currentAppsURL={currentAppsExcURL}/>
    </div>
  );
}

export default App;
