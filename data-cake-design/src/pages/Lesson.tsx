import { motion, AnimatePresence } from 'motion/react';
import { ArrowLeft, Lightbulb, Copy, Award, ChevronRight, Terminal, Database, Cloud, FolderHeart, ExternalLink, Code2, List, Hash } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useState } from 'react';
import Sidebar from '../components/Sidebar';

import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

export default function Lesson() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isTOCOpen, setIsTOCOpen] = useState(false);

  const codeSnippet = `print(10 + 3)   # 13
print(10 - 3)   # 7
print(10 * 3)   # 30
print(10 / 3)   # 3.3333333333333335
print(10 // 3)  # 3 (Floor division)
print(10 ** 3)  # 1000 (Exponentiation)
print(10 % 3)   # 1 (Modulo - remainder)`;

  const [copied, setCopied] = useState(false);

  const copyCode = () => {
    navigator.clipboard.writeText(codeSnippet);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex-1 w-full max-w-[1200px] mx-auto px-4 md:px-10 py-8 flex flex-col lg:flex-row gap-12 relative">
      {/* Mobile Nav Overlay */}
      <AnimatePresence>
        {isSidebarOpen && (
          <>
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsSidebarOpen(false)}
              className="fixed inset-0 bg-surface/80 backdrop-blur-sm z-[60] lg:hidden"
            />
            <motion.div
              initial={{ x: '-100%' }}
              animate={{ x: 0 }}
              exit={{ x: '-100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="fixed left-0 top-0 bottom-0 w-[280px] bg-surface z-[70] lg:hidden p-6 shadow-2xl overflow-y-auto"
            >
               <Sidebar isMobile onSelect={() => setIsSidebarOpen(false)} />
            </motion.div>
          </>
        )}
      </AnimatePresence>

      {/* Main Sidebar (Desktop) */}
      <div className="hidden lg:block">
        <Sidebar />
      </div>
      
      <main className="flex-1 min-w-0">
        {/* Mobile Mini Nav */}
        <div className="flex lg:hidden items-center justify-between mb-8 pb-4 border-b border-outline-variant sticky top-16 bg-surface z-30 -mx-4 px-4 pt-2">
          <button 
            onClick={() => setIsSidebarOpen(true)}
            className="flex items-center gap-2 text-on-surface-variant font-mono text-[10px] uppercase tracking-wider hover:text-on-surface transition-colors"
          >
            <List className="w-4 h-4" />
            Nav
          </button>
          
          <div className="h-4 w-px bg-outline-variant mx-2" />

          <button 
            onClick={() => setIsTOCOpen(!isTOCOpen)}
            className="flex items-center gap-2 text-on-surface-variant font-mono text-[10px] uppercase tracking-wider hover:text-on-surface transition-colors"
          >
            <Hash className="w-4 h-4" />
            Content
          </button>
          
          <div className="ml-auto flex items-center gap-2">
             <div className="text-on-surface font-mono text-[10px] font-bold">SECTION_1</div>
             <ChevronRight className="w-3 h-3 text-on-surface-variant" />
             <div className="text-on-surface font-mono text-[10px] opacity-60">OPERATORS</div>
          </div>
        </div>

        {/* Mobile TOC Drawer */}
        <AnimatePresence>
          {isTOCOpen && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="lg:hidden mb-10 overflow-hidden bg-surface-container border border-outline-variant rounded"
            >
              <div className="p-6">
                <div className="text-xs font-mono text-on-surface-variant uppercase tracking-widest mb-4">
                  On This Page
                </div>
                <nav className="flex flex-col gap-3">
                  <a href="#" onClick={() => setIsTOCOpen(false)} className="text-sm text-on-surface font-bold underline decoration-on-surface/30">Arithmetic: Basic Math</a>
                  <a href="#" onClick={() => setIsTOCOpen(false)} className="text-sm text-on-surface-variant">Comparison Operators</a>
                  <a href="#" onClick={() => setIsTOCOpen(false)} className="text-sm text-on-surface-variant">Logical Operators</a>
                </nav>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <Link to="/curriculum" className="inline-flex items-center gap-2 text-xs font-mono text-on-surface-variant hover:text-on-surface transition-colors mb-10 group mt-4 lg:mt-0">
          <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
          Back to Python
        </Link>

        <header className="mb-12">
          <div className="flex items-center gap-3 mb-2">
            <div className="h-px w-8 bg-on-surface" />
            <span className="text-xs font-mono text-on-surface-variant uppercase tracking-[0.2em]">Section 1: Foundations</span>
          </div>
          <h1 className="text-3xl md:text-5xl font-bold text-on-surface mb-6 tracking-tighter">Operators</h1>
          <p className="text-lg text-on-surface-variant max-w-3xl leading-relaxed">
            Python supports arithmetic, comparison, logical, bitwise, assignment, identity, and membership operators. They form the core logic for manipulating data structures and controlling flow.
          </p>
        </header>

        <section className="mb-16 border-l-2 border-on-surface/10 pl-4 md:pl-8 ml-0.5 pb-8">
          <div className="relative">
             <div className="absolute -left-[18px] md:-left-[34px] top-2 w-[4px] h-6 bg-on-surface" />
             <h2 className="text-2xl font-bold text-on-surface mb-6 tracking-tight">
                Arithmetic: Basic Math
             </h2>
          </div>
          
          <p className="text-on-surface-variant mb-8 leading-relaxed">
            Standard operations like addition, subtraction, multiplication, and division. Division (<code className="font-mono bg-surface-container-high px-1.5 py-0.5 rounded border border-outline-variant">/</code>) always returns a float. Floor division (<code className="font-mono bg-surface-container-high px-1.5 py-0.5 rounded border border-outline-variant">//</code>) returns an integer by discarding the fractional part.
          </p>

          <motion.div 
            whileHover={{ scale: 1.01 }}
            className="bg-[#1e1e1e] border border-outline-variant rounded-2xl overflow-hidden my-10 group shadow-lg"
          >
            <div className="flex items-center justify-between px-4 py-2 bg-[#252526] border-b border-outline-variant">
              <span className="text-xs font-mono text-zinc-400">main.py</span>
              <button 
                onClick={copyCode}
                className="text-zinc-400 hover:text-white transition-colors opacity-0 group-hover:opacity-100 flex items-center gap-2"
              >
                <span className="text-[10px]">{copied ? 'COPIED!' : 'COPY CODE'}</span>
                {copied ? <Award className="w-4 h-4 text-white" /> : <Copy className="w-4 h-4" />}
              </button>
            </div>
            <div className="p-1">
              <SyntaxHighlighter 
                language="python" 
                style={vscDarkPlus}
                customStyle={{ 
                  margin: 0, 
                  background: 'transparent',
                  padding: '1.5rem',
                  fontSize: '0.875rem'
                }}
              >
                {codeSnippet}
              </SyntaxHighlighter>
            </div>
          </motion.div>

          <div className="bg-surface-container border border-outline-variant p-6 rounded-2xl flex gap-4 items-start hover:shadow-md transition-shadow">
            <Lightbulb className="w-6 h-6 text-on-surface shrink-0 mt-0.5" />
            <div>
              <h4 className="text-xs font-mono font-bold text-on-surface mb-1 uppercase tracking-wider">Pro Tip</h4>
              <p className="text-sm text-on-surface-variant leading-relaxed">
                The modulo operator (<code className="font-mono text-on-surface">%</code>) is frequently used in technical interviews to determine if a number is even or odd (<code className="font-mono text-on-surface">n % 2 == 0</code>).
              </p>
            </div>
          </div>
        </section>

        <section className="mb-16 border-l border-outline-variant pl-4 md:pl-8 ml-0.5 pb-8">
          <div className="relative">
             <div className="absolute -left-[29px] md:-left-[45px] top-2 w-[5px] h-6 bg-outline-variant" />
             <h2 className="text-2xl font-bold text-on-surface mb-6">
                Comparison Operators
             </h2>
          </div>
          
          <p className="text-on-surface-variant mb-8 leading-relaxed">
            Used to compare values. They either return <code className="font-mono text-on-surface font-bold bg-surface-container px-1 py-0.5 rounded">True</code> or <code className="font-mono text-on-surface-variant">False</code>.
          </p>

          <div className="border border-outline-variant rounded-2xl overflow-hidden shadow-sm">
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse min-w-[400px]">
                <thead className="bg-surface-container-high border-b border-outline-variant">
                  <tr>
                    <th className="py-4 px-6 text-[10px] md:text-xs font-mono text-on-surface-variant uppercase tracking-widest">Operator</th>
                    <th className="py-4 px-6 text-[10px] md:text-xs font-mono text-on-surface-variant uppercase tracking-widest">Name</th>
                    <th className="py-4 px-6 text-[10px] md:text-xs font-mono text-on-surface-variant uppercase tracking-widest">Example</th>
                  </tr>
                </thead>
                <tbody className="text-xs md:text-sm font-mono">
                  {[
                    { op: '==', name: 'Equal', ex: 'x == y', bg: 'bg-surface' },
                    { op: '!=', name: 'Not equal', ex: 'x != y', bg: 'bg-surface-container' },
                    { op: '>', name: 'Greater than', ex: 'x > y', bg: 'bg-surface' },
                  ].map((row, i) => (
                    <motion.tr 
                      key={i}
                      whileHover={{ backgroundColor: 'var(--surface-container-highest)' }}
                      className={`border-b border-outline-variant ${row.bg} transition-colors`}
                    >
                      <td className="py-4 px-6 text-on-surface font-bold">
                        <span className="p-1 rounded bg-on-surface text-surface">{row.op}</span>
                      </td>
                      <td className="py-4 px-6 text-on-surface-variant">{row.name}</td>
                      <td className="py-4 px-6 text-on-surface-variant opacity-70 italic">{row.ex}</td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </section>
      </main>

      {/* TOC Sidebar (Desktop) */}
      <aside className="hidden lg:block w-56 shrink-0 sticky top-24 h-[calc(100vh-6rem)] overflow-y-auto">
        <div className="text-xs font-mono text-on-surface-variant uppercase tracking-widest mb-6">
          On This Page
        </div>
        <nav className="flex flex-col gap-1 border-l border-outline-variant pl-4">
          <a href="#" className="text-sm text-on-surface py-1.5 relative block font-bold">
            <span className="absolute -left-[17px] top-1/2 -translate-y-1/2 w-[2px] h-4 bg-on-surface" />
            Arithmetic: Basic Math
          </a>
          <a href="#" className="text-sm text-on-surface-variant hover:text-on-surface transition-colors py-1.5 block">Comparison Operators</a>
          <a href="#" className="text-sm text-on-surface-variant hover:text-on-surface transition-colors py-1.5 block font-mono">Logical Operators</a>
          
          <div className="mt-8 pt-8 border-t border-outline-variant">
            <span className="text-xs font-mono text-on-surface-variant uppercase tracking-widest mb-4 block">Interview Mastery</span>
            <a href="#" className="text-xs text-on-surface-variant hover:text-on-surface leading-relaxed block py-1 transition-colors">Q: What is operator precedence in Python?</a>
            <a href="#" className="text-xs text-on-surface-variant hover:text-on-surface leading-relaxed block py-1 mt-2 transition-colors">Q: How does Python's `or` operator work?</a>
          </div>
        </nav>
      </aside>
    </div>
  );
}
