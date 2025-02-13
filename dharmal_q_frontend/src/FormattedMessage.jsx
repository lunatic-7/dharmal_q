import React from "react"


const FormattedMessage = ({ content }) => {
  const formatText = (text) => {
    // Split the text into paragraphs
    const paragraphs = text.split("\n\n")

    return paragraphs.map((paragraph, index) => {
      // Replace numbered list items
      paragraph = paragraph.replace(/(\d+\.\s)(.+)/g, "<li>$2</li>")

      // Replace bold text
      paragraph = paragraph.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")

      // Replace italic text
      paragraph = paragraph.replace(/_(.*?)_/g, "<em>$1</em>")

      if (paragraph.startsWith("<li>")) {
        return <ol key={index} dangerouslySetInnerHTML={{ __html: paragraph }} />
      }

      return <p key={index} dangerouslySetInnerHTML={{ __html: paragraph }} />
    })
  }

  return <div className="formatted-message">{formatText(content)}</div>
}

export default FormattedMessage

