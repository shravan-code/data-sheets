import { ChevronRight, Code2, Database, Terminal, Calculator, FolderClosed, ExternalLink, ChevronDown } from 'lucide-react';
import { NavLink } from 'react-router-dom';
import { motion } from 'motion/react';

export default function Sidebar({ isMobile, onSelect }: { isMobile?: boolean, onSelect?: () => void }) {
  return (
    <aside className={`${isMobile ? 'w-full' : 'hidden lg:block w-64 pr-8 border-r border-outline-variant sticky top-24 h-[calc(100vh-6rem)]'} overflow-y-auto`}>
      <div className="flex flex-col gap-6">
        <div>
          <button className="w-full flex items-center justify-between px-4 py-2 rounded-xl bg-surface-container text-on-surface text-xs font-semibold border border-outline-variant hover:border-on-surface transition-colors group">
            <div className="flex items-center gap-2">
              <Code2 className="w-4 h-4 text-on-surface-variant group-hover:text-on-surface" />
              PROGRAMMING
            </div>
            <ChevronDown className="w-4 h-4 text-on-surface-variant" />
          </button>
          
          <div className="mt-2 ml-4 border-l border-outline-variant pl-4 flex flex-col gap-1">
            {[
              { name: 'Python', icon: <ChevronRight className="w-4 h-4" /> },
              { name: 'SQL', icon: null },
              { name: 'Bash', icon: null },
              { name: 'PowerShell', icon: null },
            ].map((item) => (
              <NavLink
                key={item.name}
                to={item.name === 'Python' ? '/curriculum' : '#'}
                onClick={onSelect}
                className={({ isActive }) => 
                  `block px-3 py-1.5 text-sm transition-all rounded-lg relative overflow-hidden group/link ${
                    isActive && item.name === 'Python'
                    ? 'text-on-surface font-bold bg-surface-container-highest border-l-2 border-on-surface -ml-[17px]'
                    : 'text-on-surface-variant hover:text-emerald-500 hover:bg-emerald-500/[0.03]'
                  }`
                }
              >
                <motion.span
                  className="relative z-10"
                  whileHover={{ x: 4 }}
                >
                  {item.name}
                </motion.span>
                <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/[0.05] to-transparent opacity-0 group-hover/link:opacity-100 transition-opacity" />
              </NavLink>
            ))}
          </div>
        </div>

        <div>
           <button className="w-full flex items-center justify-between px-4 py-2 rounded-xl text-on-surface-variant text-xs font-semibold hover:bg-surface-container transition-colors group">
            <div className="flex items-center gap-2">
              <Database className="w-4 h-4" />
              CONCEPTS
            </div>
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>

        <div>
           <button className="w-full flex items-center justify-between px-4 py-2 rounded-xl text-on-surface-variant text-xs font-semibold hover:bg-surface-container transition-colors group">
            <div className="flex items-center gap-2">
              <Calculator className="w-4 h-4" />
              TOOLS
            </div>
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>

        <div className="mt-auto pt-8 border-t border-outline-variant">
          <a href="#" className="flex items-center gap-2 px-3 py-2 text-sm text-on-surface hover:text-on-surface hover:bg-surface-container transition-all group rounded-xl">
            <FolderClosed className="w-4 h-4" />
            My Portfolio
            <ExternalLink className="w-3 h-3 ml-auto opacity-50 group-hover:opacity-100" />
          </a>
        </div>
      </div>
    </aside>
  );
}
