import Navbar from "./components/UI/Navbar";
import ExecutionView from "./components/Request-Execution/ExecutionView";

const ngrokURL = 'https://561c-141-3-72-67.ngrok-free.app/';

const cfd_workloadsNamesURL = ngrokURL + 'cfd_workloads';
const bfs_workloadsNamesURL = ngrokURL + 'bfs_workloads';
const requestExecutionURL = ngrokURL + 'setExecutionRequest';
const frequenciesOptionsURL = ngrokURL + 'frequencies';


function App() {
  return (
    <div>
      <Navbar/>
      <ExecutionView cfd_workloadsURL={cfd_workloadsNamesURL} bfs_workloadsURL={bfs_workloadsNamesURL} 
                    executionURL={requestExecutionURL} frequenciesURL={frequenciesOptionsURL}/>
    </div>
  );
}

export default App;
