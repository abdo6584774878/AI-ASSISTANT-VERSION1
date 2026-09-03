"use strict";

console.log("🔥 DASHBOARD.JS LOADED");

let currentConversationId = null;

document.addEventListener("DOMContentLoaded", () => {
    console.log("🔥 DASHBOARD DOM READY");

    // ============================================================
    // ELEMENTS
    // ============================================================

    const conversationsButton =
        document.getElementById("conversations-button");

    const newChatButton =
        document.getElementById("new-chat-button");

    // IMPORTANT:
    // HTML uses "conversations-list" (plural)
    const conversationList =
        document.getElementById("conversations-list");

    // Workspace
    const switchOptions =
        document.querySelectorAll(".product-switch-option");

    const chatbotNav =
        document.getElementById("chatbot-nav");

    const securityNav =
        document.getElementById("security-nav");

    const chatbotWorkspace =
        document.getElementById("chatbot-workspace");

    const securityWorkspace =
        document.getElementById("security-workspace");

    const workspaceTitle =
        document.getElementById("workspace-title");

    // Chat
    const chatInput =
        document.getElementById("chat-input");

    const sendButton =
        document.getElementById("send-button");

    const chatMessages =
        document.getElementById("chat-messages");

    console.log("🔎 Dashboard elements:", {
        conversationsButton,
        newChatButton,
        conversationList,
        switchOptions: switchOptions.length,
        chatbotNav,
        securityNav,
        chatbotWorkspace,
        securityWorkspace,
        workspaceTitle,
        chatInput,
        sendButton,
        chatMessages
    });

    // ============================================================
    // WORKSPACE SWITCHING
    // ============================================================

    function switchWorkspace(workspace) {
        console.log("🔄 Switching workspace:", workspace);

        const isChatbot = workspace === "chatbot";

        // Switch topbar buttons
        switchOptions.forEach((option) => {
            const isActive =
                option.dataset.workspace === workspace;

            option.classList.toggle("active", isActive);
            option.setAttribute(
                "aria-selected",
                isActive ? "true" : "false"
            );
        });

        // Sidebar
        if (chatbotNav) {
            chatbotNav.classList.toggle(
                "hidden",
                !isChatbot
            );
        }

        if (securityNav) {
            securityNav.classList.toggle(
                "hidden",
                isChatbot
            );
        }

        // Workspace
        if (chatbotWorkspace) {
            chatbotWorkspace.classList.toggle(
                "hidden",
                !isChatbot
            );
        }

        if (securityWorkspace) {
            securityWorkspace.classList.toggle(
                "hidden",
                isChatbot
            );
        }

        // Breadcrumb title
        if (workspaceTitle) {
            workspaceTitle.textContent = isChatbot
                ? "Chatbot"
                : "Security Analyzer";
        }

        console.log(
            "✅ Workspace switched to:",
            workspace
        );
    }

    switchOptions.forEach((option) => {
        option.addEventListener("click", (event) => {
            event.preventDefault();

            const workspace =
                option.dataset.workspace;

            if (!workspace) {
                console.error(
                    "❌ Product switch button has no data-workspace"
                );
                return;
            }

            switchWorkspace(workspace);
        });
    });

    // Start in chatbot
    switchWorkspace("chatbot");

    // ============================================================
    // ADD MESSAGE
    // ============================================================

    function addMessage(role, text) {
        if (!chatMessages) {
            return null;
        }

        const message =
            document.createElement("div");

        message.className =
            `chat-message chat-message-${role}`;

        const content =
            document.createElement("div");

        content.className =
            "chat-message-content";

        content.textContent =
            text ?? "";

        message.appendChild(content);
        chatMessages.appendChild(message);

        chatMessages.scrollTop =
            chatMessages.scrollHeight;

        return message;
    }

    // ============================================================
    // LOADING MESSAGE
    // ============================================================

    function addLoadingMessage() {
        if (!chatMessages) {
            return;
        }

        removeLoadingMessage();

        const message =
            document.createElement("div");

        message.className =
            "chat-message chat-message-assistant";

        message.id =
            "ai-loading-message";

        const content =
            document.createElement("div");

        content.className =
            "chat-message-content";

        content.textContent =
            "Veyra is thinking...";

        message.appendChild(content);
        chatMessages.appendChild(message);

        chatMessages.scrollTop =
            chatMessages.scrollHeight;
    }

    function removeLoadingMessage() {
        const loadingMessage =
            document.getElementById(
                "ai-loading-message"
            );

        if (loadingMessage) {
            loadingMessage.remove();
        }
    }
    // ============================================================
    // RENDER CONVERSATIONS
    // ============================================================

    function renderConversations(conversations) {
        if (!conversationList) {
            return;
        }

        conversationList.innerHTML = "";

        if (!conversations || conversations.length === 0) {
            conversationList.innerHTML = `
            <div class="conversation-empty">
                No conversations yet
            </div>
        `;
            return;
        }

        conversations.forEach((conversation) => {
            const item = document.createElement("div");

            item.className = "conversation-item";
            item.dataset.conversationId = conversation.id;

            if (
                currentConversationId !== null &&
                Number(conversation.id) ===
                Number(currentConversationId)
            ) {
                item.classList.add("active");
            }

            item.innerHTML = `
            <button
                type="button"
                class="conversation-title"
                title="${escapeHtml(conversation.title)}"
            >
                <span>◷</span>
                <span>
                    ${escapeHtml(conversation.title)}
                </span>
            </button>

            <button
                type="button"
                class="conversation-menu"
                aria-label="Conversation options"
                aria-expanded="false"
            >
                ⋯
            </button>

            <div class="conversation-dropdown hidden">
                <button
                    type="button"
                    class="conversation-action rename-action"
                >
                    <span>✎</span>
                    <span>Rename</span>
                </button>

                <button
                    type="button"
                    class="conversation-action delete-action"
                >
                    <span>⌫</span>
                    <span>Delete</span>
                </button>
            </div>
        `;

            // --------------------------------------------------------
            // OPEN CONVERSATION
            // --------------------------------------------------------

            const titleButton =
                item.querySelector(".conversation-title");

            if (titleButton) {
                titleButton.addEventListener("click", () => {
                    openConversation(conversation.id);
                });
            }

            // --------------------------------------------------------
            // MENU
            // --------------------------------------------------------

            const menuButton =
                item.querySelector(".conversation-menu");

            const dropdown =
                item.querySelector(".conversation-dropdown");

            if (menuButton && dropdown) {
                menuButton.addEventListener("click", (event) => {
                    event.stopPropagation();

                    // Close every other menu first
                    document
                        .querySelectorAll(".conversation-dropdown")
                        .forEach((menu) => {
                            if (menu !== dropdown) {
                                menu.classList.add("hidden");
                            }
                        });

                    document
                        .querySelectorAll(".conversation-menu")
                        .forEach((button) => {
                            if (button !== menuButton) {
                                button.setAttribute(
                                    "aria-expanded",
                                    "false"
                                );
                            }
                        });

                    dropdown.classList.toggle("hidden");

                    menuButton.setAttribute(
                        "aria-expanded",
                        dropdown.classList.contains("hidden")
                            ? "false"
                            : "true"
                    );
                });
            }

            // --------------------------------------------------------
            // RENAME
            // --------------------------------------------------------

            const renameButton =
                item.querySelector(".rename-action");

            if (renameButton) {
                renameButton.addEventListener("click", (event) => {
                    event.stopPropagation();

                    dropdown.classList.add("hidden");
                    menuButton.setAttribute(
                        "aria-expanded",
                        "false"
                    );

                    renameConversation(
                        conversation.id,
                        conversation.title
                    );
                });
            }

            // --------------------------------------------------------
            // DELETE
            // --------------------------------------------------------

            const deleteButton =
                item.querySelector(".delete-action");

            if (deleteButton) {
                deleteButton.addEventListener("click", (event) => {
                    event.stopPropagation();

                    dropdown.classList.add("hidden");
                    menuButton.setAttribute(
                        "aria-expanded",
                        "false"
                    );

                    deleteConversation(
                        conversation.id,
                        conversation.title
                    );
                });
            }

            conversationList.appendChild(item);
        });
    }
    // ============================================================
    // RENAME CONVERSATION
    // ============================================================

    async function renameConversation(conversationId, currentTitle) {
        const newTitle = window.prompt(
            "Rename conversation:",
            currentTitle
        );

        if (newTitle === null) {
            return;
        }

        const title = newTitle.trim();

        if (!title) {
            window.alert("Conversation title cannot be empty.");
            return;
        }

        if (title === currentTitle) {
            return;
        }

        try {
            console.log(
                "✏️ Renaming conversation:",
                conversationId,
                title
            );

            const response = await fetch(
                `${API_BASE_URL}/api/conversations/${conversationId}`,
                {
                    method: "PUT",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        title: title
                    })
                }
            );

            const data = await response.json();

            console.log(
                "✏️ Rename response:",
                data
            );

            if (!response.ok || !data.success) {
                window.alert(
                    data.message ||
                    "Could not rename conversation."
                );
                return;
            }

            await loadConversations();

            console.log(
                "✅ Conversation renamed successfully"
            );

        } catch (error) {
            console.error(
                "🔥 Rename conversation error:",
                error
            );

            window.alert(
                "Unable to rename conversation."
            );
        }
    }
    // ============================================================
    // DELETE CONVERSATION
    // ============================================================

    async function deleteConversation(
        conversationId,
        conversationTitle
    ) {
        const confirmed = window.confirm(
            `Delete "${conversationTitle}"?\n\nThis will permanently delete the conversation and its messages.`
        );

        if (!confirmed) {
            return;
        }

        try {
            console.log(
                "🗑️ Deleting conversation:",
                conversationId
            );

            const response = await fetch(
                `${API_BASE_URL}/api/conversations/${conversationId}`,
                {
                    method: "DELETE",
                    credentials: "include"
                }
            );

            const data = await response.json();

            console.log(
                "🗑️ Delete response:",
                data
            );

            if (!response.ok || !data.success) {
                window.alert(
                    data.message ||
                    "Could not delete conversation."
                );
                return;
            }

            // --------------------------------------------------------
            // If the deleted conversation was active
            // --------------------------------------------------------

            if (
                Number(currentConversationId) ===
                Number(conversationId)
            ) {
                currentConversationId = null;

                if (chatMessages) {
                    chatMessages.innerHTML = "";
                }

                if (chatInput) {
                    chatInput.value = "";
                    chatInput.style.height = "auto";
                }
            }

            // Refresh sidebar
            await loadConversations();

            console.log(
                "✅ Conversation deleted successfully"
            );

        } catch (error) {
            console.error(
                "🔥 Delete conversation error:",
                error
            );

            window.alert(
                "Unable to delete conversation."
            );
        }
    }
    // ============================================================
    // ESCAPE HTML
    // ============================================================

    function escapeHtml(value) {
        const div =
            document.createElement("div");

        div.textContent =
            value ?? "";

        return div.innerHTML;
    }

    // ============================================================
    // LOAD CONVERSATIONS
    // ============================================================

    async function loadConversations() {
        if (!conversationList) {
            console.error(
                "❌ #conversations-list not found"
            );
            return;
        }

        try {
            console.log(
                "📚 Loading conversations..."
            );

            const response =
                await fetch(
                    `${API_BASE_URL}/api/conversations`,
                    {
                        method: "GET",
                        credentials: "include"
                    }
                );

            console.log(
                "📡 Conversations status:",
                response.status
            );

            const data =
                await response.json();

            console.log(
                "📚 Conversations response:",
                data
            );

            if (!response.ok || !data.success) {
                console.error(
                    "❌ Could not load conversations:",
                    data.message
                );
                return;
            }

            renderConversations(
                data.conversations || []
            );

        } catch (error) {
            console.error(
                "🔥 Failed to load conversations:",
                error
            );
        }
    }

    // ============================================================
    // RENAME CONVERSATION
    // ============================================================

    async function renameConversation(conversationId, currentTitle) {
        const newTitle = window.prompt(
            "Rename conversation:",
            currentTitle
        );

        if (newTitle === null) {
            return;
        }

        const title = newTitle.trim();

        if (!title) {
            window.alert("Conversation title cannot be empty.");
            return;
        }

        if (title === currentTitle) {
            return;
        }

        try {
            console.log(
                "✏️ Renaming conversation:",
                conversationId,
                title
            );

            const response = await fetch(
                `${API_BASE_URL}/api/conversations/${conversationId}`,
                {
                    method: "PUT",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        title: title
                    })
                }
            );

            const data = await response.json();

            console.log(
                "✏️ Rename response:",
                data
            );

            if (!response.ok || !data.success) {
                window.alert(
                    data.message ||
                    "Could not rename conversation."
                );
                return;
            }

            await loadConversations();

            console.log(
                "✅ Conversation renamed successfully"
            );

        } catch (error) {
            console.error(
                "🔥 Rename conversation error:",
                error
            );

            window.alert(
                "Unable to rename conversation."
            );
        }
    }

    // ============================================================
    // OPEN CONVERSATION
    // ============================================================

    async function openConversation(conversationId) {
        try {
            console.log(
                "📂 Opening conversation:",
                conversationId
            );

            const response =
                await fetch(
                    `${API_BASE_URL}/api/conversations/${conversationId}`,
                    {
                        method: "GET",
                        credentials: "include"
                    }
                );

            const data =
                await response.json();

            console.log(
                "📂 Conversation response:",
                data
            );

            if (!response.ok || !data.success) {
                console.error(
                    "❌ Could not open conversation:",
                    data.message
                );
                return;
            }

            currentConversationId =
                Number(data.conversation.id);

            // Clear current chat
            if (chatMessages) {
                chatMessages.innerHTML = "";
            }

            // Render messages
            const messages =
                data.conversation.messages || [];

            messages.forEach((message) => {
                addMessage(
                    message.role === "user"
                        ? "user"
                        : "assistant",
                    message.content
                );
            });

            // Refresh sidebar
            await loadConversations();

            if (chatInput) {
                chatInput.focus();
            }

            console.log(
                "✅ Conversation opened:",
                currentConversationId
            );

        } catch (error) {
            console.error(
                "🔥 Failed to open conversation:",
                error
            );
        }
    }

    // ============================================================
    // CREATE NEW CHAT
    // ============================================================

    async function createNewChat() {
        console.log(
            "🆕 New Chat button clicked"
        );

        try {
            const response =
                await fetch(
                    `${API_BASE_URL}/api/conversations`,
                    {
                        method: "POST",
                        credentials: "include",
                        headers: {
                            "Content-Type":
                                "application/json"
                        },
                        body: JSON.stringify({
                            title:
                                "New Conversation"
                        })
                    }
                );

            console.log(
                "📡 Create conversation status:",
                response.status
            );

            const data =
                await response.json();

            console.log(
                "🆕 New conversation response:",
                data
            );

            if (!response.ok || !data.success) {
                console.error(
                    "❌ Could not create conversation:",
                    data.message
                );
                return;
            }

            currentConversationId =
                Number(data.conversation.id);

            // Clear chat
            if (chatMessages) {
                chatMessages.innerHTML = "";
            }

            // Clear input
            if (chatInput) {
                chatInput.value = "";
                chatInput.style.height = "auto";
                chatInput.focus();
            }

            // Refresh conversations
            await loadConversations();

            console.log(
                "✅ New conversation created:",
                currentConversationId
            );

        } catch (error) {
            console.error(
                "🔥 Failed to create conversation:",
                error
            );
        }
    }

    // ============================================================
    // SEND MESSAGE
    // ============================================================

    async function sendMessage() {
        if (!chatInput) {
            return;
        }

        const message =
            chatInput.value.trim();

        if (!message) {
            return;
        }

        console.log(
            "📤 Sending message:",
            message
        );

        chatInput.disabled = true;

        if (sendButton) {
            sendButton.disabled = true;
        }

        addMessage(
            "user",
            message
        );

        chatInput.value = "";
        chatInput.style.height = "auto";

        addLoadingMessage();

        try {
            const response =
                await fetch(
                    `${API_BASE_URL}/api/chat`,
                    {
                        method: "POST",
                        credentials: "include",
                        headers: {
                            "Content-Type":
                                "application/json"
                        },
                        body: JSON.stringify({
                            message: message,
                            conversation_id:
                                currentConversationId
                        })
                    }
                );

            const data =
                await response.json();

            console.log(
                "📥 Chat response:",
                data
            );

            removeLoadingMessage();

            if (!response.ok || !data.success) {
                if (
                    data.message ===
                    "Not authenticated."
                ) {
                    window.location.href =
                        "login.html";
                    return;
                }

                addMessage(
                    "error",
                    data.message ||
                    "Something went wrong."
                );

                return;
            }

            currentConversationId =
                Number(
                    data.conversation_id
                );

            addMessage(
                "assistant",
                data.response
            );

            await loadConversations();

        } catch (error) {
            console.error(
                "🔥 Chat error:",
                error
            );

            removeLoadingMessage();

            addMessage(
                "error",
                "Unable to connect to Veyra."
            );

        } finally {
            chatInput.disabled = false;

            if (sendButton) {
                sendButton.disabled = false;
            }

            chatInput.focus();
        }
    }

    // ============================================================
    // SEND BUTTON
    // ============================================================

    if (sendButton) {
        sendButton.addEventListener(
            "click",
            sendMessage
        );
    }

    // ============================================================
    // CHAT INPUT
    // ============================================================

    if (chatInput) {
        chatInput.addEventListener(
            "keydown",
            (event) => {
                if (
                    event.key === "Enter" &&
                    !event.shiftKey
                ) {
                    event.preventDefault();
                    sendMessage();
                }
            }
        );

        chatInput.addEventListener(
            "input",
            () => {
                chatInput.style.height = "auto";

                chatInput.style.height =
                    `${chatInput.scrollHeight}px`;
            }
        );
    }

    // ============================================================
    // NEW CHAT BUTTON
    // ============================================================

    if (newChatButton) {
        newChatButton.addEventListener(
            "click",
            createNewChat
        );

        console.log(
            "✅ New Chat listener attached"
        );
    } else {
        console.error(
            "❌ #new-chat-button not found"
        );
    }

    // ============================================================
    // CONVERSATIONS BUTTON
    // ============================================================

    if (conversationsButton) {
        conversationsButton.addEventListener(
            "click",
            () => {
                console.log(
                    "📚 Conversations button clicked"
                );

                if (!conversationList) {
                    console.error(
                        "❌ #conversations-list not found"
                    );
                    return;
                }

                conversationList.classList.toggle(
                    "hidden"
                );
            }
        );

        console.log(
            "✅ Conversations listener attached"
        );
    } else {
        console.error(
            "❌ #conversations-button not found"
        );
    }
    // ============================================================
    // CLOSE CONVERSATION MENUS WHEN CLICKING OUTSIDE
    // ============================================================

    document.addEventListener("click", () => {
        document
            .querySelectorAll(".conversation-dropdown")
            .forEach((menu) => {
                menu.classList.add("hidden");
            });

        document
            .querySelectorAll(".conversation-menu")
            .forEach((button) => {
                button.setAttribute(
                    "aria-expanded",
                    "false"
                );
            });
    });
    // ============================================================
    // INITIALIZE
    // ============================================================

    loadConversations();

    console.log(
        "🔥 Veyra dashboard initialized"
    );
});