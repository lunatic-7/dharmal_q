import { motion, AnimatePresence } from "framer-motion"
import * as ScrollArea from "@radix-ui/react-scroll-area"
import FormattedMessage from "./FormattedMessage"

function ChatArea({ chat, character, chatEndRef }) {
  return (
    <ScrollArea.Root className="h-96 overflow-hidden">
      <ScrollArea.Viewport className="w-full h-full">
        <div className="p-4 space-y-4">
          <AnimatePresence>
            {chat.map((msg, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
                className={`p-3 max-w-xs rounded-lg text-sm shadow-md ${
                  msg.sender === "User" ? "ml-auto bg-blue-500 text-white" : "mr-auto bg-gray-600 text-gray-200"
                }`}
              >
                <strong className="block text-xs text-gray-400 mb-1">
                  {msg.sender === "User" ? "You" : character}
                </strong>
                <FormattedMessage content={msg.text} />
              </motion.div>
            ))}
          </AnimatePresence>
          <div ref={chatEndRef} />
        </div>
      </ScrollArea.Viewport>
      <ScrollArea.Scrollbar
        className="flex select-none touch-none p-0.5 bg-gray-700 transition-colors duration-150 ease-out hover:bg-gray-600 data-[orientation=vertical]:w-2.5 data-[orientation=horizontal]:flex-col data-[orientation=horizontal]:h-2.5"
        orientation="vertical"
      >
        <ScrollArea.Thumb className="flex-1 bg-gray-500 rounded-[10px] relative before:content-[''] before:absolute before:top-1/2 before:left-1/2 before:-translate-x-1/2 before:-translate-y-1/2 before:w-full before:h-full before:min-w-[44px] before:min-h-[44px]" />
      </ScrollArea.Scrollbar>
    </ScrollArea.Root>
  )
}

export default ChatArea
