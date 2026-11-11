import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, ShieldCheck, Sparkles, Table, Download, FileText } from 'lucide-react';
import { CitationItem, ResearchGapItem } from '../services/api';

interface Message {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  citations?: CitationItem[];
  gaps?: ResearchGapItem[];
  comparison?: any;
}

interface ChatPanelProps {
  selectedPaperIds: string[];
  onNavigateCitation: (page: number, paperId: string) => void;
}

export const ChatPanel: React.FC<ChatPanelProps> = ({
  selectedPaperIds,
  onNavigateCitation,
}) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      sender: 'assistant',
      text: 'Welcome to ReSearch_Mate. Ask questions about your uploaded research papers, compare methodologies, or discover research gaps. All claims are verified against page citations.',
    },
  ]);
  const [query, setQuery] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [agentStatus, setAgentStatus] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, agentStatus]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || isStreaming) return;

    const userMsg: Message = {
      id: `msg-${Date.now()}`,
      sender: 'user',
      text: query,
    };

    const assistantMsgId = `asst-${Date.now()}`;
    const assistantMsg: Message = {
      id: assistantMsgId,
      sender: 'assistant',
      text: '',
      citations: [],
      gaps: [],
    };

    setMessages((prev) => [...prev, userMsg, assistantMsg]);
    const currentQuery = query;
    setQuery('');
    setIsStreaming(true);
    setAgentStatus('RetrievalAgent: Searching indexed chunks...');

    try {
      const response = await fetch('/api/chat/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: currentQuery,
          paper_ids: selectedPaperIds,
          stream: true,
          top_k: 5,
        }),
      });

      if (!response.body) return;
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let accumulatedText = '';
      const citationsList: CitationItem[] = [];
      const gapsList: ResearchGapItem[] = [];
      let comparisonData: any = null;

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunkText = decoder.decode(value, { stream: true });
        const lines = chunkText.split('\n');

        let currentEvent = 'message';
        for (const line of lines) {
          if (line.startsWith('event: ')) {
            currentEvent = line.slice(7).trim();
          } else if (line.startsWith('data: ')) {
            const dataStr = line.slice(6).trim();
            if (!dataStr) continue;

            try {
              const data = JSON.parse(dataStr);
              if (currentEvent === 'agent_status') {
                setAgentStatus(`${data.agent}: ${data.status}`);
              } else if (currentEvent === 'token') {
                accumulatedText += data.chunk;
              } else if (currentEvent === 'citation') {
                citationsList.push(data);
              } else if (currentEvent === 'research_gap') {
                gapsList.push(data);
              } else if (currentEvent === 'comparison') {
                comparisonData = data;
              } else if (currentEvent === 'done') {
                setAgentStatus(null);
              }
            } catch (err) {
              // Non-JSON token
              accumulatedText += dataStr;
            }

            setMessages((prev) =>
              prev.map((m) =>
                m.id === assistantMsgId
                  ? {
                      ...m,
                      text: accumulatedText,
                      citations: [...citationsList],
                      gaps: [...gapsList],
                      comparison: comparisonData,
                    }
                  : m
              )
            );
          }
        }
      }
    } catch (err) {
      console.error('Chat error:', err);
    } finally {
      setIsStreaming(false);
      setAgentStatus(null);
    }
  };

  return (
    <div className="flex-1 h-full flex flex-col bg-slate-950 border-r border-slate-800">
      {/* Header */}
      <div className="h-14 px-6 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Bot className="w-5 h-5 text-emerald-400" />
          <span className="font-semibold text-slate-200">Multi-Agent Research Chat</span>
        </div>
        <div className="flex items-center gap-3">
          {agentStatus && (
            <div className="flex items-center gap-2 text-xs text-emerald-400 bg-emerald-950/60 border border-emerald-800 px-3 py-1 rounded-full animate-pulse">
              <Sparkles className="w-3.5 h-3.5" />
              <span>{agentStatus}</span>
            </div>
          )}
          <div className="flex items-center gap-1.5">
            <button
              onClick={async () => {
                const res = await fetch('/api/chat/export?format=markdown', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ query: 'Academic Literature Review', paper_ids: selectedPaperIds, stream: false })
                });
                const blob = await res.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'literature_review.md';
                a.click();
              }}
              className="px-2.5 py-1 text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 rounded flex items-center gap-1 transition border border-slate-700"
              title="Download literature review in Markdown"
            >
              <Download className="w-3 h-3 text-emerald-400" />
              <span>Export MD</span>
            </button>
            <button
              onClick={async () => {
                const res = await fetch('/api/chat/export?format=latex', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ query: 'Academic Literature Review', paper_ids: selectedPaperIds, stream: false })
                });
                const blob = await res.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'literature_review.tex';
                a.click();
              }}
              className="px-2.5 py-1 text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 rounded flex items-center gap-1 transition border border-slate-700"
              title="Download literature review in LaTeX"
            >
              <FileText className="w-3 h-3 text-sky-400" />
              <span>LaTeX</span>
            </button>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((m) => (
          <div
            key={m.id}
            className={`flex flex-col ${
              m.sender === 'user' ? 'items-end' : 'items-start'
            }`}
          >
            <div
              className={`max-w-2xl p-4 rounded-xl text-sm leading-relaxed ${
                m.sender === 'user'
                  ? 'bg-emerald-600 text-white rounded-br-none'
                  : 'bg-slate-900 border border-slate-800 text-slate-200 rounded-bl-none'
              }`}
            >
              <div>{m.text}</div>

              {/* Citations Badges */}
              {m.citations && m.citations.length > 0 && (
                <div className="mt-4 pt-3 border-t border-slate-800">
                  <div className="text-xs font-semibold text-slate-400 mb-2 flex items-center gap-1">
                    <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                    <span>Verified Citations ({m.citations.length}):</span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {m.citations.map((c, idx) => (
                      <button
                        key={idx}
                        onClick={() => onNavigateCitation(c.page_number, c.paper_id)}
                        className="px-2.5 py-1 text-xs bg-slate-800 hover:bg-emerald-900/60 border border-slate-700 hover:border-emerald-500 text-emerald-300 rounded flex items-center gap-1 transition"
                        title={c.quote}
                      >
                        <span className="font-mono font-semibold">[p. {c.page_number}]</span>
                        <span className="text-slate-400 max-w-xs truncate">{c.paper_title}</span>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Comparison Matrix Display */}
              {m.comparison && (
                <div className="mt-4 pt-3 border-t border-slate-800">
                  <div className="text-xs font-semibold text-slate-400 mb-2 flex items-center gap-1">
                    <Table className="w-3.5 h-3.5 text-sky-400" />
                    <span>Comparative Matrix:</span>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="w-full text-xs text-left border border-slate-800">
                      <thead className="bg-slate-800/60 text-slate-300">
                        <tr>
                          <th className="p-2 border-b border-slate-800">Aspect</th>
                          {m.comparison.papers.map((p: string, i: number) => (
                            <th key={i} className="p-2 border-b border-slate-800">{p}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {m.comparison.aspects.map((aspect: string, i: number) => (
                          <tr key={i} className="border-b border-slate-800/40">
                            <td className="p-2 font-medium text-slate-300 bg-slate-900/40">{aspect}</td>
                            {m.comparison.papers.map((_: any, pi: number) => (
                              <td key={pi} className="p-2 text-slate-400">Extracted and verified</td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* Research Gaps */}
              {m.gaps && m.gaps.length > 0 && (
                <div className="mt-4 pt-3 border-t border-slate-800">
                  <div className="text-xs font-semibold text-amber-400 mb-1 flex items-center gap-1">
                    <Sparkles className="w-3.5 h-3.5" />
                    <span>Potential Research Gap:</span>
                  </div>
                  {m.gaps.map((g, gi) => (
                    <div key={gi} className="text-xs text-slate-400 bg-amber-950/20 border border-amber-900/40 p-2.5 rounded-lg mt-1">
                      <div className="font-semibold text-amber-300">{g.area}</div>
                      <div>{g.description}</div>
                      <div className="mt-1 text-slate-300 font-medium">Direction: {g.potential_direction}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="p-4 border-t border-slate-800 bg-slate-900/60">
        <div className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={
              selectedPaperIds.length > 0
                ? `Ask across ${selectedPaperIds.length} selected paper(s)...`
                : 'Ask a research question across all indexed papers...'
            }
            disabled={isStreaming}
            className="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-emerald-500"
          />
          <button
            type="submit"
            disabled={isStreaming || !query.trim()}
            className="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-800 text-white font-medium rounded-lg flex items-center justify-center transition"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </form>
    </div>
  );
};
