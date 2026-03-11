import { useState } from "react";
import axios from "axios";

function App() {

  const [file, setFile] = useState(null)
  const [email, setEmail] = useState("")
  const [summary, setSummary] = useState("")

  const uploadFile = async () => {

    const formData = new FormData()

    formData.append("file", file)
    formData.append("email", email)

    try {

      const res = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData
      )

      setSummary(res.data.summary)

    } catch (error) {

      setSummary("Error contacting backend")

    }

  }

  return (

    <div style={{padding:40}}>

      <h1>Sales Insight Automator</h1>

      <input
        type="file"
        onChange={(e)=>setFile(e.target.files[0])}
      />

      <br/><br/>

      <input
        placeholder="Enter Email"
        value={email}
        onChange={(e)=>setEmail(e.target.value)}
      />

      <br/><br/>

      <button onClick={uploadFile}>
        Upload & Generate Summary
      </button>

      <br/><br/>

      <h3>AI Summary</h3>

      <p>{summary}</p>

    </div>

  )
}

export default App