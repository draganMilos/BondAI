import React, { useState } from 'react';
import ToneSlider from './components/ToneSlider';
import DraftCard from './components/DraftCard';
import { getDrafts, createPersona, sendFeedback } from './api';

export default function App(){
  const [userId] = useState('demo-user-123');
  const [personaId, setPersonaId] = useState<string | null>(null);
  const [incoming, setIncoming] = useState('Hey! Loved your travel pics — where was that beach?');
  const [snippets, setSnippets] = useState('Dubai Marina; likes hiking; dog named Coco');
  const [tone, setTone] = useState(0);
  const [options, setOptions] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  async function ensurePersona(){
    if (personaId) return personaId;
    const p = await createPersona({
      display_name: 'Alex', tone: 'playful', cadence: 'short', emoji_policy: 'light',
      boundaries: ['no explicit sexual content', 'no politics'], goals: ['build rapport', 'coffee date'], disclosure: false
    }, userId);
    setPersonaId(p.id); return p.id;
  }

  async function fetchDrafts(){
    setLoading(true);
    try{
      const pid = await ensurePersona();
      const res = await getDrafts({
        user_id: userId, persona_id: pid, incoming_text: incoming,
        context_snippets: snippets.split(';').map(s=>s.trim()).filter(Boolean),
        num_options: 4, tone_bias: tone
      }, userId);
      setOptions(res.options);
    }catch(e:any){
      alert(e.message || 'Error');
    }finally{ setLoading(false); }
  }

  return (
    <div style={{maxWidth: 720, margin: '24px auto', fontFamily: 'ui-sans-serif'}}>
      <h1>Dating Co‑Pilot (Draft Assistant)</h1>
      <p>Paste the latest message below. We’ll suggest short, respectful, playful replies you can edit and send yourself.</p>

      <label>Incoming message</label>
      <textarea value={incoming} onChange={e=>setIncoming(e.target.value)} rows={4} style={{width:'100%'}} />

      <label>Context snippets (semicolon separated)</label>
      <input value={snippets} onChange={e=>setSnippets(e.target.value)} style={{width:'100%'}} />

      <ToneSlider value={tone} onChange={setTone} />

      <button disabled={loading} onClick={fetchDrafts}>{loading? 'Thinking…' : 'Get drafts'}</button>

      <div style={{marginTop:16}}>
        {options.map((o, i)=> (
          <DraftCard key={i} text={(o.disclosure? o.text + `\n\n(${o.disclosure})` : o.text)} rationale={o.rationale}
            onApprove={()=>sendFeedback({user_id: userId, draft_text: o.text, action:'approved'}, userId)}
            onReject={()=>sendFeedback({user_id: userId, draft_text: o.text, action:'rejected'}, userId)}
          />
        ))}
      </div>
    </div>
  );
}
