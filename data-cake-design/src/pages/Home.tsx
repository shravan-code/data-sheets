import { Terminal, ArrowRight, Code2, GitMerge, DraftingCompass } from 'lucide-react';
import { motion } from 'motion/react';
import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div className="w-full">
      <section className="w-full max-w-[1200px] mx-auto px-4 md:px-10 py-24 md:py-32 border-b border-outline-variant relative overflow-hidden">
        {/* IDE Grid Overlay */}
        <div 
          className="absolute top-0 right-0 w-1/2 h-full border-l border-outline-variant opacity-20 pointer-events-none" 
          style={{ 
            backgroundImage: 'radial-gradient(circle at 2px 2px, var(--on-surface-variant) 1px, transparent 0)', 
            backgroundSize: '32px 32px' 
          }}
        />

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-2xl relative z-10"
        >
          <div className="flex items-center gap-2 mb-6">
            <Terminal className="w-4 h-4 text-on-surface" />
            <span className="text-sm text-on-surface font-mono font-bold bg-surface-container px-2 py-1 rounded-md ring-1 ring-outline-variant">{'>'} ./init_career.sh</span>
          </div>
          
          <h1 className="text-4xl md:text-5xl font-bold text-on-surface mb-6 leading-tight">
            Master the Stack.<br />
            Ace the Interview.
          </h1>
          
          <p className="text-lg text-on-surface-variant mb-10 border-l-2 border-outline-variant pl-6 leading-relaxed">
            A developer-first learning platform engineered like your favorite IDE. 
            No fluff, just pure technical signal. Level up your system design, algorithms, and backend architecture.
          </p>
          
          <div className="flex flex-col sm:flex-row items-start gap-4">
            <motion.div
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Link 
                to="/curriculum"
                className="bg-on-surface text-surface px-10 py-4 text-sm font-bold hover:shadow-[0_0_30px_rgba(16,185,129,0.3)] transition-all uppercase tracking-widest rounded-full block relative overflow-hidden group/btn"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-emerald-600 via-emerald-500 to-emerald-600 opacity-0 group-hover/btn:opacity-100 transition-opacity" />
                <span className="relative z-10">Get Started</span>
              </Link>
            </motion.div>
            
            <motion.button 
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-transparent border-2 border-outline-variant text-on-surface px-10 py-4 text-sm font-bold hover:border-emerald-500 hover:text-emerald-500 transition-all uppercase tracking-widest rounded-full relative overflow-hidden group/btn2"
            >
              <div className="absolute inset-0 bg-emerald-500/5 opacity-0 group-hover/btn2:opacity-100 transition-opacity" />
              <span className="relative z-10">View Curriculum</span>
            </motion.button>
          </div>
        </motion.div>
      </section>

      <section className="w-full max-w-[1200px] mx-auto px-4 md:px-10 py-16 md:py-24">
        <div className="flex items-center gap-2 mb-10 border-b border-outline-variant pb-4">
          <span className="text-sm font-mono text-on-surface-variant">#</span>
          <h2 className="text-sm font-mono text-on-surface-variant uppercase tracking-[0.2em]">Featured_Paths</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <PathCard 
            id="01"
            title="Python Backend"
            desc="Build scalable APIs, master asynchronous IO, and understand internal memory management deeply."
            icon={<Code2 className="w-8 h-8 text-on-surface group-hover:text-emerald-500 transition-colors" />}
            color="emerald"
          />
          <PathCard 
            id="02"
            title="Data Structures"
            desc="Deep dive into trees, graphs, and advanced algorithmic patterns required for top-tier engineering roles."
            icon={<GitMerge className="w-8 h-8 text-on-surface group-hover:text-blue-500 transition-colors" />}
            color="blue"
          />
          <PathCard 
            id="03"
            title="System Design"
            desc="Architect distributed systems, handle massive scale gracefully, and dominate the whiteboarding phase."
            icon={<DraftingCompass className="w-8 h-8 text-on-surface group-hover:text-amber-500 transition-colors" />}
            color="amber"
          />
        </div>
      </section>
    </div>
  );
}

function PathCard({ id, title, desc, icon, color }: { id: string, title: string, desc: string, icon: React.ReactNode, color: 'emerald' | 'blue' | 'amber' }) {
  const colorMap = {
    emerald: 'from-emerald-500 via-emerald-400 to-emerald-600 group-hover:shadow-[0_0_30px_rgba(16,185,129,0.15)]',
    blue: 'from-blue-500 via-blue-400 to-blue-600 group-hover:shadow-[0_0_30px_rgba(59,130,246,0.15)]',
    amber: 'from-amber-500 via-amber-400 to-amber-600 group-hover:shadow-[0_0_30px_rgba(245,158,11,0.15)]'
  };

  const iconBorderMap = {
    emerald: 'group-hover:border-emerald-500',
    blue: 'group-hover:border-blue-500',
    amber: 'group-hover:border-amber-500'
  };

  const textMap = {
    emerald: 'group-hover:text-emerald-500',
    blue: 'group-hover:text-blue-500',
    amber: 'group-hover:text-amber-500'
  };

  return (
    <motion.div
      whileHover={{ y: -8 }}
      transition={{ type: 'spring', stiffness: 300, damping: 20 }}
    >
      <Link 
        to="/curriculum"
        className={`border border-outline-variant bg-surface-container p-8 hover:border-transparent transition-all group relative overflow-hidden flex flex-col h-full rounded-2xl ${colorMap[color]}`}
      >
        <div className={`absolute top-0 left-0 w-full h-[6px] bg-gradient-to-r ${colorMap[color].split(' ')[0]} ${colorMap[color].split(' ')[1]} ${colorMap[color].split(' ')[2]} transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left`} />
        
        <div className="flex justify-between items-start mb-6 relative z-10">
          <div className={`p-3 rounded-xl bg-surface border border-outline-variant transition-all duration-300 shadow-sm ${iconBorderMap[color]}`}>
            {icon}
          </div>
          <span className={`text-xs font-mono text-on-surface-variant transition-colors duration-300 ${textMap[color]}`}>[{id}]</span>
        </div>
        
        <h3 className="text-xl font-bold text-on-surface mb-2 tracking-tight group-hover:translate-x-1 transition-transform relative z-10">{title}</h3>
        <p className="text-sm text-on-surface-variant mb-8 flex-grow leading-relaxed group-hover:text-on-surface transition-colors relative z-10">
          {desc}
        </p>
        
        <div className="inline-flex items-center gap-2 text-sm font-mono text-on-surface font-bold mt-auto group-hover:gap-4 transition-all relative z-10">
          <span className={`p-1 rounded text-surface text-[10px] opacity-0 group-hover:opacity-100 transition-opacity ${color === 'emerald' ? 'bg-emerald-500' : color === 'blue' ? 'bg-blue-500' : 'bg-amber-500'}`}>READY</span>
          <span className={textMap[color]}>EXEC_MODULE</span>
          <ArrowRight className={`w-4 h-4 opacity-0 group-hover:opacity-100 -translate-x-2 group-hover:translate-x-0 transition-all ${textMap[color]}`} />
        </div>

        {/* Dynamic background glow on hover */}
        <div className={`absolute -bottom-10 -right-10 w-32 h-32 opacity-0 group-hover:opacity-[0.08] rounded-full blur-3xl transition-opacity pointer-events-none ${color === 'emerald' ? 'bg-emerald-500' : color === 'blue' ? 'bg-blue-500' : 'bg-amber-500'}`} />
      </Link>
    </motion.div>
  );
}
