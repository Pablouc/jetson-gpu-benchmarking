import Navbar from "./components/UI/Navbar";
import ExecutionView from "./components/Request-Execution/ExecutionView";

const appsNamesURL = 'http://127.0.0.1:5000/appsNames';
const workloadsNamesURL = 'http://127.0.0.1:5000/workloadsNames';
const requestExecutionURL = 'http://127.0.0.1:5000/setExecutionRequest'


function App() {
  return (
    <div>
      <Navbar></Navbar>
      <ExecutionView appsURL={appsNamesURL}  workloadsURL={workloadsNamesURL} executionURL={requestExecutionURL}></ExecutionView>
    </div>
  );
}

export default App;
