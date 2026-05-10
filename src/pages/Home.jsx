import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

export default function Home() {
  const navigate = useNavigate();

  return (
    <motion.section 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20, transition: { duration: 0.3 } }}
      transition={{ duration: 0.6 }}
      className="relative min-h-[70vh] flex flex-col items-center justify-center overflow-x-hidden pt-10 pb-20"
    >
      <div className="relative z-10 w-full max-w-4xl mx-auto px-6 text-center">
        <div className="mb-6 inline-block">
          <span className="px-4 py-2 bg-red-600/20 text-red-400 rounded-full text-sm font-semibold border border-red-500/30 shadow-[0_0_20px_rgba(220,38,38,0.2)]">
            ✨ Powered by Advanced AI
          </span>
        </div>

        <h1 className="text-6xl md:text-7xl font-bold mb-6 leading-tight">
          Discover Your Next
          <span className="bg-gradient-to-r from-red-400 via-red-600 to-red-900 text-transparent bg-clip-text drop-shadow-[0_0_30px_rgba(220,38,38,0.3)]"> Cinematic Masterpiece</span>
        </h1>

        <p className="text-xl md:text-2xl text-gray-300 mb-12 max-w-2xl mx-auto leading-relaxed">
          Experience personalized movie recommendations powered by cutting-edge AI technology. Explore films tailored to your unique taste.
        </p>

        <div className="flex flex-col sm:flex-row gap-6 justify-center">
          <button className="px-8 py-4 bg-gradient-to-r from-red-600 to-black text-white rounded-xl font-bold text-lg border border-red-500/50 btn-primary">
            Neural Network
          </button>
          
          <button 
            onClick={() => navigate('/imdb')}
            id="imdbListBtn" 
            className="px-8 py-4 bg-gradient-to-r from-black via-red-900 to-red-600 text-white rounded-xl font-bold text-lg border border-red-500/50 btn-secondary"
          >
            IMDB List
          </button>
          
          <button className="px-8 py-4 bg-gradient-to-r from-red-800 to-black text-white rounded-xl font-bold text-lg border border-red-500/50 btn-primary">
            Movies Dossier
          </button>
        </div>
      </div>
    </motion.section>
  );
}
