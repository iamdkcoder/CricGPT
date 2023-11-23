import {React ,useEffect} from "react";
import axios from "axios";

function ApiOutput(message) {

    useEffect(()=>{
        const requestBody = {
            "message": message
        }
        // axios.post("https://cricgpt-n6lr75fo6q-el.a.run.app/chat",requestBody)
        axios.post("http://127.0.0.0:8000/chat",requestBody)
        .then((response)=>{
            console.log(response)
            return response
        })
        .catch((error)=>{
            console.error('Error fetching data:', error);
        })
    },[]);

}

export default ApiOutput;