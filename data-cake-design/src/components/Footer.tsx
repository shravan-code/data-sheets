import { Code2 } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-surface border-t border-outline-variant w-full mt-auto">
      <div className="flex flex-col md:flex-row justify-between items-center px-4 md:px-10 py-8 w-full max-w-[1200px] mx-auto gap-4">
        <div className="flex flex-col items-center md:items-start gap-1">
          <div className="flex items-center gap-2 text-on-surface">
            <Code2 className="w-5 h-5" />
            <span className="font-bold text-lg uppercase tracking-wider">Data Cake</span>
          </div>
          <span className="text-[10px] uppercase font-mono tracking-widest text-on-surface-variant opacity-60">© 2024 Data Cake. Dev-first learning.</span>
        </div>
        
        <div className="flex flex-wrap justify-center gap-4 md:gap-8 text-[10px] uppercase font-mono tracking-widest text-on-surface-variant">
          {['Documentation', 'Changelog', 'Status', 'Privacy'].map((item) => (
            <a key={item} href="#" className="hover:text-on-surface hover:underline transition-all underline-offset-4">
              {item}
            </a>
          ))}
        </div>
      </div>
    </footer>
  );
}
