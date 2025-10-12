export const renderDescription = (text) => {
    if (!text) return null;

    const urlRegex = /((?:https?:\/\/|www\.)[^\s]+)/g;
    const parts = text.split(urlRegex);

    return parts.map((part, index) => {
        if (urlRegex.test(part)) {
            const href = part.startsWith("http") ? part : `https://${part}`;
            return (
                <a
                    key={index}
                    href={href}
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    {part}
                </a>
            );
        }
        return <span key={index}>{part}</span>;
    });
};
