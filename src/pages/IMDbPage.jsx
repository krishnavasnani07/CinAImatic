import React from 'react';
import { motion } from 'framer-motion';

const movieCategories = [
    { title: "🔥 ACTION MOVIES 🔥", movies: [
        { title: "John Wick", rating: "8.4", year: "2014", img: "https://placehold.co/400x600/111111/ff4500?text=John+Wick" },
        { title: "Mad Max: Fury Road", rating: "8.1", year: "2015", img: "https://placehold.co/400x600/111111/ff4500?text=Mad+Max" },
        { title: "Extraction", rating: "6.7", year: "2020", img: "https://placehold.co/400x600/111111/ff4500?text=Extraction" },
        { title: "The Dark Knight", rating: "9.0", year: "2008", img: "https://placehold.co/400x600/111111/ff4500?text=Dark+Knight" },
        { title: "Gladiator", rating: "8.5", year: "2000", img: "https://placehold.co/400x600/111111/ff4500?text=Gladiator" },
        { title: "Mission Impossible", rating: "7.7", year: "2018", img: "https://placehold.co/400x600/111111/ff4500?text=Mission+Imp" },
        { title: "Top Gun: Maverick", rating: "8.3", year: "2022", img: "https://placehold.co/400x600/111111/ff4500?text=Top+Gun" },
        { title: "Avengers: Endgame", rating: "8.4", year: "2019", img: "https://placehold.co/400x600/111111/ff4500?text=Avengers" },
        { title: "Die Hard", rating: "8.2", year: "1988", img: "https://placehold.co/400x600/111111/ff4500?text=Die+Hard" },
        { title: "The Raid", rating: "7.6", year: "2011", img: "https://placehold.co/400x600/111111/ff4500?text=The+Raid" },
        { title: "Fast & Furious 7", rating: "7.1", year: "2015", img: "https://placehold.co/400x600/111111/ff4500?text=Fast+7" },
        { title: "300", rating: "7.6", year: "2006", img: "https://placehold.co/400x600/111111/ff4500?text=300" },
        { title: "Terminator 2", rating: "8.6", year: "1991", img: "https://placehold.co/400x600/111111/ff4500?text=Terminator+2" },
        { title: "Casino Royale", rating: "8.0", year: "2006", img: "https://placehold.co/400x600/111111/ff4500?text=Casino+Royale" },
        { title: "Edge of Tomorrow", rating: "7.9", year: "2014", img: "https://placehold.co/400x600/111111/ff4500?text=Edge+of+Tomorrow" }
    ]},
    { title: "😂 COMEDY MOVIES 😂", movies: [
        { title: "The Hangover", rating: "7.7", year: "2009", img: "https://placehold.co/400x600/111111/ff4500?text=The+Hangover" },
        { title: "Free Guy", rating: "7.1", year: "2021", img: "https://placehold.co/400x600/111111/ff4500?text=Free+Guy" },
        { title: "Jumanji", rating: "6.9", year: "1995", img: "https://placehold.co/400x600/111111/ff4500?text=Jumanji" },
        { title: "Superbad", rating: "7.6", year: "2007", img: "https://placehold.co/400x600/111111/ff4500?text=Superbad" },
        { title: "Deadpool", rating: "8.0", year: "2016", img: "https://placehold.co/400x600/111111/ff4500?text=Deadpool" },
        { title: "21 Jump Street", rating: "7.2", year: "2012", img: "https://placehold.co/400x600/111111/ff4500?text=21+Jump+St" },
        { title: "Home Alone", rating: "7.7", year: "1990", img: "https://placehold.co/400x600/111111/ff4500?text=Home+Alone" },
        { title: "Ted", rating: "6.9", year: "2012", img: "https://placehold.co/400x600/111111/ff4500?text=Ted" },
        { title: "The Mask", rating: "6.9", year: "1994", img: "https://placehold.co/400x600/111111/ff4500?text=The+Mask" },
        { title: "Central Intelligence", rating: "6.3", year: "2016", img: "https://placehold.co/400x600/111111/ff4500?text=Central+Int" },
        { title: "Rush Hour", rating: "7.0", year: "1998", img: "https://placehold.co/400x600/111111/ff4500?text=Rush+Hour" },
        { title: "Yes Man", rating: "6.8", year: "2008", img: "https://placehold.co/400x600/111111/ff4500?text=Yes+Man" },
        { title: "We're the Millers", rating: "7.0", year: "2013", img: "https://placehold.co/400x600/111111/ff4500?text=The+Millers" },
        { title: "Johnny English", rating: "6.2", year: "2003", img: "https://placehold.co/400x600/111111/ff4500?text=Johnny+English" },
        { title: "Mr. Bean's Holiday", rating: "6.4", year: "2007", img: "https://placehold.co/400x600/111111/ff4500?text=Mr+Bean" }
    ]},
    { title: "🚀 SCI-FI MOVIES 🚀", movies: [
        { title: "Interstellar", rating: "8.7", year: "2014", img: "https://placehold.co/400x600/111111/ff4500?text=Interstellar" },
        { title: "Inception", rating: "8.8", year: "2010", img: "https://placehold.co/400x600/111111/ff4500?text=Inception" },
        { title: "The Matrix", rating: "8.7", year: "1999", img: "https://placehold.co/400x600/111111/ff4500?text=The+Matrix" },
        { title: "Avatar", rating: "7.9", year: "2009", img: "https://placehold.co/400x600/111111/ff4500?text=Avatar" },
        { title: "Blade Runner 2049", rating: "8.0", year: "2017", img: "https://placehold.co/400x600/111111/ff4500?text=Blade+Runner" },
        { title: "Dune", rating: "8.0", year: "2021", img: "https://placehold.co/400x600/111111/ff4500?text=Dune" },
        { title: "Star Wars", rating: "8.6", year: "1977", img: "https://placehold.co/400x600/111111/ff4500?text=Star+Wars" },
        { title: "Gravity", rating: "7.7", year: "2013", img: "https://placehold.co/400x600/111111/ff4500?text=Gravity" },
        { title: "The Martian", rating: "8.0", year: "2015", img: "https://placehold.co/400x600/111111/ff4500?text=The+Martian" },
        { title: "Ready Player One", rating: "7.4", year: "2018", img: "https://placehold.co/400x600/111111/ff4500?text=Ready+Player" },
        { title: "Arrival", rating: "7.9", year: "2016", img: "https://placehold.co/400x600/111111/ff4500?text=Arrival" },
        { title: "Tenet", rating: "7.3", year: "2020", img: "https://placehold.co/400x600/111111/ff4500?text=Tenet" },
        { title: "Ex Machina", rating: "7.7", year: "2014", img: "https://placehold.co/400x600/111111/ff4500?text=Ex+Machina" },
        { title: "Oblivion", rating: "7.0", year: "2013", img: "https://placehold.co/400x600/111111/ff4500?text=Oblivion" },
        { title: "Edge of Tomorrow", rating: "7.9", year: "2014", img: "https://placehold.co/400x600/111111/ff4500?text=Edge+of+Tomorrow" }
    ]},
    { title: "❤️ ROMANCE MOVIES ❤️", movies: [
        { title: "Titanic", rating: "7.9", year: "1997", img: "https://placehold.co/400x600/111111/ff4500?text=Titanic" },
        { title: "La La Land", rating: "8.0", year: "2016", img: "https://placehold.co/400x600/111111/ff4500?text=La+La+Land" },
        { title: "The Notebook", rating: "7.8", year: "2004", img: "https://placehold.co/400x600/111111/ff4500?text=Notebook" },
        { title: "Me Before You", rating: "7.4", year: "2016", img: "https://placehold.co/400x600/111111/ff4500?text=Me+Before+You" },
        { title: "Pride & Prejudice", rating: "7.8", year: "2005", img: "https://placehold.co/400x600/111111/ff4500?text=Pride" },
        { title: "A Walk to Remember", rating: "7.3", year: "2002", img: "https://placehold.co/400x600/111111/ff4500?text=A+Walk" },
        { title: "Dear John", rating: "6.3", year: "2010", img: "https://placehold.co/400x600/111111/ff4500?text=Dear+John" },
        { title: "The Fault in Our Stars", rating: "7.7", year: "2014", img: "https://placehold.co/400x600/111111/ff4500?text=Fault+in+Stars" },
        { title: "Before Sunrise", rating: "8.1", year: "1995", img: "https://placehold.co/400x600/111111/ff4500?text=Sunrise" },
        { title: "Crazy Rich Asians", rating: "6.9", year: "2018", img: "https://placehold.co/400x600/111111/ff4500?text=Crazy+Rich" },
        { title: "500 Days of Summer", rating: "7.7", year: "2009", img: "https://placehold.co/400x600/111111/ff4500?text=500+Days" },
        { title: "Love Actually", rating: "7.6", year: "2003", img: "https://placehold.co/400x600/111111/ff4500?text=Love+Actually" },
        { title: "Notting Hill", rating: "7.2", year: "1999", img: "https://placehold.co/400x600/111111/ff4500?text=Notting+Hill" },
        { title: "Your Name", rating: "8.4", year: "2016", img: "https://placehold.co/400x600/111111/ff4500?text=Your+Name" },
        { title: "The Vow", rating: "6.8", year: "2012", img: "https://placehold.co/400x600/111111/ff4500?text=The+Vow" }
    ]}
];

const containerVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.2 }
  }
};

const itemVariants = {
  hidden: { opacity: 0, y: 30 },
  show: { opacity: 1, y: 0, transition: { duration: 0.8, ease: "easeOut" } }
};

export default function IMDbPage() {
  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 1.05, transition: { duration: 0.3 } }}
      transition={{ duration: 0.5 }}
      className="relative z-10 w-full px-6 pt-16 pb-20"
    >
      <div className="max-w-7xl mx-auto text-center mb-16">
        <h1 className="text-5xl font-bold text-white mb-4 drop-shadow-[0_0_15px_rgba(255,69,0,0.8)]">
          IMDb Masterpiece Collection
        </h1>
        <p className="text-gray-400 text-lg">Explore the highest-rated cinematic journeys of all time.</p>
      </div>

      <motion.div 
        variants={containerVariants}
        initial="hidden"
        animate="show"
        className="max-w-7xl mx-auto space-y-24 text-left"
      >
        {movieCategories.map((cat, index) => (
          <motion.div key={index} variants={itemVariants} className="movie-category">
            <h2 className="text-2xl sm:text-3xl font-bold text-center mb-8 tracking-widest text-[#ff4500] drop-shadow-[0_0_15px_rgba(255,69,0,0.8)] whitespace-nowrap">
              <span className="text-orange-500/50 hidden sm:inline">🟧━━━━━━━━━━</span> 
              {cat.title} 
              <span className="text-orange-500/50 hidden sm:inline">━━━━━━━━━━🟧</span>
            </h2>
            <div className="flex overflow-x-auto gap-6 pb-8 snap-x snap-mandatory hide-scrollbar px-4 sm:px-0">
              {cat.movies.map((movie, mIndex) => (
                <div key={mIndex} className="min-w-[220px] sm:min-w-[280px] snap-start glass-card rounded-2xl overflow-hidden movie-card-hover group cursor-pointer border border-white/5 relative flex-shrink-0 bg-black/40">
                  <div className="absolute inset-0 bg-gradient-to-t from-black via-black/40 to-transparent opacity-80 z-10 group-hover:opacity-40 transition-opacity"></div>
                  <img src={movie.img} alt={movie.title} className="w-full h-[330px] sm:h-[420px] object-cover group-hover:scale-110 transition-transform duration-700" />
                  <div className="absolute bottom-0 left-0 right-0 p-5 z-20 transform translate-y-2 group-hover:translate-y-0 transition-transform duration-300">
                    <h3 className="text-lg sm:text-xl font-bold text-white mb-1 group-hover:text-[#ff7b00] transition-colors truncate">{movie.title}</h3>
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-yellow-500 font-bold tracking-wider drop-shadow-[0_0_5px_rgba(234,179,8,0.5)]">⭐ {movie.rating}</span>
                      <span className="text-gray-300 font-medium">{movie.year}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        ))}
      </motion.div>
    </motion.div>
  );
}
