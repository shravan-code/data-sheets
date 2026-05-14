import { motion, AnimatePresence } from 'motion/react';
import { Terminal, Code, Database, Calculator, UserCircle2, ChevronRight, Award, List } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useState } from 'react';
import Sidebar from '../components/Sidebar';

export default function Curriculum() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  return (
    <div className="flex-1 flex w-full max-w-[1200px] mx-auto px-4 md:px-10 py-8 relative">
      {/* Mobile Sidebar Overlay */}
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

      <div className="hidden lg:block">
        <Sidebar />
      </div>
      
      <main className="flex-1 lg:pl-12">
        {/* Mobile Page Header with Toggle */}
        <div className="flex lg:hidden items-center justify-between mb-8 pb-4 border-b border-outline-variant sticky top-16 bg-surface z-30 -mx-4 px-4 pt-2">
          <button 
            onClick={() => setIsSidebarOpen(true)}
            className="flex items-center gap-2 text-on-surface-variant font-mono text-xs hover:text-on-surface transition-colors"
          >
            <List className="w-5 h-5" />
            MODULE_INDEX
          </button>
          <div className="text-on-surface font-mono text-xs font-bold ring-1 ring-outline-variant px-2 py-1 rounded">PYTHON_MASTERY</div>
        </div>

        <section className="flex flex-col items-center text-center mb-16 pt-8">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-outline-variant bg-surface-container text-on-surface-variant text-xs font-semibold mb-6">
             <Award className="w-3.5 h-3.5" />
             EXPERT DOCUMENTATION
          </div>
          <h1 className="text-3xl md:text-4xl font-bold mb-6 max-w-3xl text-on-surface">
            Python <span className="bg-on-surface text-surface px-3 py-1 rounded-lg">Mastery</span>
          </h1>
          <p className="text-lg text-on-surface-variant max-w-2xl mx-auto leading-relaxed">
            A comprehensive, interview-ready Python guide covering all concepts from fundamentals to advanced internals, with code examples, inputs/outputs, and interview Q&A.
          </p>
        </section>

        <section className="mb-16">
          <div className="flex items-center gap-4 mb-10">
            <div className="w-10 h-10 rounded-xl border border-on-surface flex items-center justify-center text-on-surface font-bold text-xl bg-surface-container shadow-[2px_2px_0_0_rgba(0,0,0,1)] dark:shadow-[2px_2px_0_0_rgba(255,255,255,1)]">
              1
            </div>
            <h2 className="text-2xl font-bold text-on-surface font-mono tracking-tight uppercase">Foundations</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <LessonCard 
              to="/lesson"
              title="Introduction to Python"
              tag="Concepts"
              readTime="5 min read"
              icon={<Code className="w-5 h-5" />}
            />
            <LessonCard 
              to="/lesson"
              title="Variables & Data Types"
              tag="Core"
              readTime="10 min read"
              icon={<UserCircle2 className="w-5 h-5" />}
            />
            <LessonCard 
              to="/lesson"
              title="Operators"
              tag="Logic"
              readTime="8 min read"
              icon={<Calculator className="w-5 h-5" />}
            />
            <LessonCard 
              to="/lesson"
              title="Strings — All Methods"
              tag="Deep Dive"
              readTime="15 min read"
              icon={<Terminal className="w-5 h-5" />}
            />
          </div>
        </section>

        {/* Timeline visualization */}
        <section className="mb-24 relative pl-12 md:pl-16">
          <div className="absolute left-0 top-0 bottom-0 flex flex-col items-center w-8">
            <div className="w-8 h-8 rounded-full bg-surface-container-highest border border-outline-variant flex items-center justify-center text-on-surface-variant text-xs font-mono z-10 scale-90">2</div>
            <div className="w-px h-full bg-outline-variant my-2" />
          </div>
          
          <h2 className="text-xl font-bold text-on-surface mb-8 flex items-center gap-3">
             <span className="text-on-surface font-mono opacity-50">#</span> Control & Iteration
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
             <div className="bg-surface-container border border-outline-variant rounded-2xl p-6 flex flex-col gap-4 opacity-50 border-dashed">
                <div className="w-8 h-8 rounded-lg bg-surface border border-outline-variant flex items-center justify-center">
                   <ChevronRight className="w-4 h-4" />
                </div>
                <div className="text-on-surface-variant text-sm font-mono uppercase tracking-wider">Module Locked</div>
             </div>
          </div>
        </section>
      </main>
    </div>
  );
}

function LessonCard({ to, title, tag, readTime, icon }: { to: string, title: string, tag: string, readTime: string, icon: React.ReactNode }) {
  return (
    <motion.div
      whileHover={{ y: -4 }}
      transition={{ type: 'spring', stiffness: 300 }}
    >
      <Link 
        to={to}
        className="block p-6 rounded-2xl bg-surface-container border border-outline-variant hover:border-emerald-500/50 transition-all group relative overflow-hidden h-full"
      >
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/[0.03] to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
        
        <div className="flex items-start gap-6 relative z-10">
          <div className="w-12 h-12 rounded-xl bg-surface border border-outline-variant flex items-center justify-center text-on-surface-variant group-hover:text-emerald-500 group-hover:border-emerald-500 transition-all shadow-sm shrink-0">
            {icon}
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <span className="px-2 py-0.5 rounded bg-on-surface text-surface group-hover:bg-emerald-500 transition-colors text-[10px] font-mono font-bold uppercase tracking-widest">{tag}</span>
              <span className="text-[10px] font-mono text-on-surface-variant/60">{readTime}</span>
            </div>
            <h3 className="text-lg font-bold text-on-surface group-hover:translate-x-1 transition-transform tracking-tight">{title}</h3>
          </div>
          <ChevronRight className="w-5 h-5 text-on-surface-variant group-hover:text-emerald-500 group-hover:translate-x-1 transition-all mt-1" />
        </div>

        {/* Dynamic underline animation */}
        <div className="absolute bottom-0 left-0 w-full h-[3px] bg-emerald-500 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left" />
      </Link>
    </motion.div>
  );
}
