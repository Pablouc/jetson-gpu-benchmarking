import MainView from "./components/MainView/MainView";

const ngrokURL = 'http://127.0.0.1:5000/';

const cfd_workloadsNamesURL = ngrokURL + 'cfd_workloads';
const bfs_workloadsNamesURL = ngrokURL + 'bfs_workloads';
const requestExecutionURL = ngrokURL + 'setExecutionRequest';
const frequenciesOptionsURL = ngrokURL + 'frequencies';
const resultsFileDataURL = ngrokURL + 'get-csv';


function App() {
  return (
    <div>
      <MainView cfd_workloadsURL={cfd_workloadsNamesURL} bfs_workloadsURL={bfs_workloadsNamesURL} 
                      executionURL={requestExecutionURL} frequenciesURL={frequenciesOptionsURL} 
                      resultsFileURL={resultsFileDataURL}/>
    </div>
  );
}

export default App;
