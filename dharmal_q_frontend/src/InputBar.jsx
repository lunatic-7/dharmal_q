import { motion } from "framer-motion"
import { FaPaperPlane } from "react-icons/fa"
import * as Tooltip from "@radix-ui/react-tooltip"

function InputBar({ userMessage, setUserMessage, sendMessage, loading }) {
  return (
    <div className="p-4 bg-gray-700">
      <div className="flex items-center space-x-2">
        <input
          type="text"
          className="flex-1 p-3 border border-gray-600 bg-gray-800 rounded-lg placeholder-gray-400 text-white focus:outline-none focus:ring-2 focus:ring-yellow-400 transition-all duration-300"
          placeholder="Type your message..."
          value={userMessage}
          onChange={(e) => setUserMessage(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          disabled={loading}
        />
        <Tooltip.Provider>
          <Tooltip.Root>
            <Tooltip.Trigger asChild>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={sendMessage}
                className={`p-3 rounded-lg font-bold transition-colors duration-300 ${
                  loading ? "bg-gray-600 cursor-not-allowed" : "bg-yellow-500 hover:bg-yellow-600"
                }`}
                disabled={loading}
              >
                {loading ? (
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Number.POSITIVE_INFINITY, ease: "linear" }}
                  >
                    <FaPaperPlane className="text-gray-300" />
                  </motion.div>
                ) : (
                  <FaPaperPlane />
                )}
              </motion.button>
            </Tooltip.Trigger>
            <Tooltip.Portal>
              <Tooltip.Content className="bg-gray-700 text-white p-2 rounded-lg shadow-md" sideOffset={5}>
                Send message
                <Tooltip.Arrow className="fill-gray-700" />
              </Tooltip.Content>
            </Tooltip.Portal>
          </Tooltip.Root>
        </Tooltip.Provider>
      </div>
    </div>
  )
}

export default InputBar
