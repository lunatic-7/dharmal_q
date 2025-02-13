import { motion } from "framer-motion"

const characters = ["Iron Man", "Yoda", "Joker", "Harry Potter", "Babu Rao"]	

function CharacterSelection({ character, setCharacter }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="flex items-center justify-between p-4 bg-gray-700"
    >
      <span className="text-lg font-semibold text-gray-300">Chat as:</span>
      <select
        className="p-2 bg-gray-600 border border-gray-500 rounded-md text-white font-semibold focus:outline-none focus:ring-2 focus:ring-yellow-400 transition-all duration-300"
        value={character}
        onChange={(e) => setCharacter(e.target.value)}
      >
        {characters.map((char) => (
          <option key={char} value={char}>
            {char}
          </option>
        ))}
      </select>
    </motion.div>
  )
}

export default CharacterSelection