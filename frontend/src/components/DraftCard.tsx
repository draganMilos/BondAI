import React from 'react';

type Props = { text: string; rationale?: string; onApprove: ()=>void; onReject: ()=>void; };
export default function DraftCard({ text, rationale, onApprove, onReject }: Props){
  return (
    <div style={{border: '1px solid #ddd', borderRadius: 12, padding: 12, marginBottom: 12}}>
      <div style={{whiteSpace:'pre-wrap'}}>{text}</div>
      {rationale && <div style={{opacity:0.7, fontSize:12, marginTop:8}}>Why: {rationale}</div>}
      <div style={{display:'flex', gap:8, marginTop:12}}>
        <button onClick={onApprove}>Approve</button>
        <button onClick={onReject}>Reject</button>
      </div>
    </div>
  );
}
