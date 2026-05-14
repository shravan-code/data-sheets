import { Link, useLocation } from 'react-router-dom';
import { Terminal, UserCircle2, Code2, Menu, X, Sun, Moon } from 'lucide-react';
import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';

export default function Navbar() {
  const location = useLocation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [theme, setTheme] = useState<'light' | 'dark'>(
    () => (localStorage.getItem('theme') as 'light' | 'dark') || 'dark'
  );

  useEffect(() => {
    const root = window.document.documentElement;
    if (theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  const links = [
    { name: 'Learning Paths', path: '/curriculum' },
    { name: 'Interview Prep', path: '#' },
    { name: 'Practice', path: '/lesson' },
  ];

  // Close menu on navigation
  useEffect(() => {
    setIsMenuOpen(false);
  }, [location.pathname]);

  // Prevent scroll when menu is open
  useEffect(() => {
    if (isMenuOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
  }, [isMenuOpen]);

  return (
    <nav className="bg-surface border-b border-outline-variant sticky top-0 z-50">
      <div className="flex justify-between items-center px-4 md:px-10 h-16 w-full max-w-[1200px] mx-auto">
        <Link to="/" className="flex items-center gap-2 group relative z-50">
          <div className="relative">
            <Code2 className="w-6 h-6 text-on-surface fill-on-surface/10 transition-all duration-500 group-hover:text-emerald-500 group-hover:fill-emerald-500/20 group-hover:scale-110" />
            <div className="absolute inset-0 bg-emerald-500 blur-lg opacity-0 group-hover:opacity-20 transition-opacity" />
          </div>
          <span className="font-bold text-xl text-on-surface uppercase tracking-wider group-hover:text-emerald-500 transition-colors">
            Data Cake
          </span>
        </Link>

        {/* Desktop Links */}
        <div className="hidden md:flex items-center gap-8 h-full">
          {links.map((link) => (
            <Link
              key={link.name}
              to={link.path}
              className={`text-sm h-full flex items-center transition-all duration-300 relative group/nav ${
                location.pathname === link.path 
                  ? 'text-on-surface font-bold' 
                  : 'text-on-surface-variant hover:text-emerald-500'
              }`}
            >
              {link.name}
              <div className={`absolute bottom-0 left-0 w-full h-[2px] transition-all duration-500 origin-left ${
                location.pathname === link.path 
                  ? 'bg-on-surface scale-x-100' 
                  : 'bg-emerald-500 scale-x-0 group-hover/nav:scale-x-100'
              }`} />
            </Link>
          ))}
        </div>

        <div className="flex items-center gap-4 text-on-surface-variant relative z-50">
          <button 
            onClick={toggleTheme}
            className="p-2 hover:bg-surface-container rounded-lg transition-colors text-on-surface"
            aria-label="Toggle theme"
          >
            {theme === 'light' ? <Moon className="w-5 h-5" /> : <Sun className="w-5 h-5" />}
          </button>
          
          <button className="hidden sm:block hover:text-on-surface transition-colors">
            <Terminal className="w-5 h-5" />
          </button>
          <button className="hidden sm:block hover:text-on-surface transition-colors">
            <UserCircle2 className="w-6 h-6" />
          </button>
          
          {/* Mobile Menu Toggle */}
          <button 
            className="md:hidden p-2 hover:bg-surface-container rounded-lg transition-colors"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu Overlay */}
      <AnimatePresence>
        {isMenuOpen && (
          <motion.div
            initial={{ opacity: 0, x: '100%' }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="fixed inset-0 top-[64px] bg-surface z-40 md:hidden flex flex-col p-6"
          >
            <div className="flex flex-col gap-6">
              {links.map((link) => (
                <Link
                  key={link.name}
                  to={link.path}
                  className={`text-xl font-bold transition-colors ${
                    location.pathname === link.path 
                      ? 'text-on-surface underline decoration-on-surface decoration-2' 
                      : 'text-on-surface opacity-60'
                  }`}
                >
                  {link.name}
                </Link>
              ))}
            </div>

            <div className="mt-10 pt-10 border-t border-outline-variant flex flex-col gap-6">
              <div className="flex items-center gap-4 text-on-surface-variant">
                <UserCircle2 className="w-8 h-8" />
                <div>
                  <div className="font-bold text-on-surface">Guest User</div>
                  <div className="text-sm opacity-60">Level 1 Junior Dev</div>
                </div>
              </div>
              <button className="w-full bg-on-surface text-surface py-4 font-bold uppercase tracking-widest text-sm rounded-xl">
                Login / Register
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
}
