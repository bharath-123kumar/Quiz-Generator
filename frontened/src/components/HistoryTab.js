import React, { useEffect, useState } from "react";
import { getHistory, getQuiz } from "../api";
import DetailsModal from "./DetailsModal";

export default function HistoryTab(){
  const [data, setData] = useState([]);
  const [loading,setLoading]=useState(true);
  const [selected, setSelected] = useState(null);
  const [detail, setDetail] = useState(null);

  useEffect(()=>{ getHistory().then(d=>{ setData(d); setLoading(false); }).catch(()=>setLoading(false)); }, []);

  async function openDetails(id){
    setSelected(id);
    const q = await getQuiz(id);
    setDetail(q);
  }

  return (
    <div>
      {loading ? <div>Loading...</div> :
        <table style={{width:'100%', borderCollapse:'collapse'}}>
          <thead><tr><th>Id</th><th>Title</th><th>URL</th><th>Created</th><th>Action</th></tr></thead>
          <tbody>
            {data.map(row => (
              <tr key={row.id}>
                <td>{row.id}</td>
                <td>{row.title}</td>
                <td style={{maxWidth:400, overflow:'hidden', textOverflow:'ellipsis'}}>{row.url}</td>
                <td>{new Date(row.created_at).toLocaleString()}</td>
                <td><button onClick={()=>openDetails(row.id)}>Details</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      }
      {detail && <DetailsModal data={detail} onClose={()=>{ setDetail(null); setSelected(null); }} />}
    </div>
  );
}
