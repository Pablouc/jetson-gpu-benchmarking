import Navbar from "./components/UI/Navbar";
import ExecutionView from "./components/Request-Execution/ExecutionView";

const ngrokURL = 'https://914a-141-3-72-67.ngrok-free.app/';

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
