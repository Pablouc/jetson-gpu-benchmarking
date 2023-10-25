import Navbar from "./components/UI/Navbar";
import ExecutionView from "./components/Request-Execution/ExecutionView";

const ngrokURL = 'http://127.0.0.1:5000/';

const cfd_workloadsNamesURL = ngrokURL + 'cfd_workloads';
const bfs_workloadsNamesURL = ngrokURL + 'bfs_workloads';
const requestExecutionURL = ngrokURL + 'setExecutionRequest'


function App() {
  return (
    <div>
      <Navbar></Navbar>
      <ExecutionView cfd_workloadsURL={cfd_workloadsNamesURL} bfs_workloadsURL={bfs_workloadsNamesURL} executionURL={requestExecutionURL}></ExecutionView>
    </div>
  );
}

export default App;
