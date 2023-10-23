import Navbar from "./components/UI/Navbar";
import ExecutionView from "./components/Request-Execution/ExecutionView";

const ngrokURL = 'http://127.0.0.1:5000/';

const appsNamesURL = ngrokURL + 'appsNames';
const workloadsNamesURL = ngrokURL + 'workloadsNames';
const requestExecutionURL = ngrokURL + 'setExecutionRequest'


function App() {
  return (
    <div>
      <Navbar></Navbar>
      <ExecutionView appsURL={appsNamesURL}  workloadsURL={workloadsNamesURL} executionURL={requestExecutionURL}></ExecutionView>
    </div>
  );
}

export default App;
