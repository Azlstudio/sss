#include "mainwindow.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QListWidgetItem>
#include <QInputDialog>
#include <QMessageBox>
#include <QApplication>
#include <QPalette>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), apiKeySet(false), messageCount(0)
{
    setWindowTitle("NextAI - Professional AI Chat");
    setGeometry(100, 100, 900, 700);

    aiService = new AIService(this);
    storageService = new StorageService(this);

    setupUI();
    setupConnections();
    applyDarkTheme();
    loadHistory();

    connect(inputField, &QLineEdit::returnPressed, this, &MainWindow::onReturnPressed);
}

MainWindow::~MainWindow()
{
}

void MainWindow::setupUI()
{
    QWidget *centralWidget = new QWidget(this);
    setCentralWidget(centralWidget);

    QVBoxLayout *mainLayout = new QVBoxLayout(centralWidget);
    mainLayout->setContentsMargins(10, 10, 10, 10);
    mainLayout->setSpacing(10);

    // Header
    QHBoxLayout *headerLayout = new QHBoxLayout();
    titleLabel = new QLabel("Next AI", this);
    titleLabel->setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;");

    clearButton = new QPushButton("Clear", this);
    clearButton->setFixedWidth(80);
    apiKeyButton = new QPushButton("API Key", this);
    apiKeyButton->setFixedWidth(80);

    headerLayout->addWidget(titleLabel);
    headerLayout->addStretch();
    headerLayout->addWidget(apiKeyButton);
    headerLayout->addWidget(clearButton);

    // Messages Area
    messagesWidget = new QListWidget(this);
    messagesWidget->setStyleSheet(
        "QListWidget { background-color: #000000; border: 1px solid #333333; }"
        "QListWidget::item { background-color: #000000; }"
        "QScrollBar:vertical { background-color: #1a1a1a; width: 8px; }"
        "QScrollBar::handle:vertical { background-color: #333333; border-radius: 4px; }"
    );

    // Input Area
    QHBoxLayout *inputLayout = new QHBoxLayout();
    inputField = new QLineEdit(this);
    inputField->setPlaceholderText("Type your message...");
    inputField->setMinimumHeight(40);
    inputField->setStyleSheet(
        "QLineEdit { background-color: #1a1a1a; color: #ffffff; border: 1px solid #333333; "
        "padding: 8px; border-radius: 5px; }"
        "QLineEdit:focus { border: 1px solid #555555; }"
    );

    sendButton = new QPushButton("Send", this);
    sendButton->setFixedWidth(80);
    sendButton->setFixedHeight(40);

    inputLayout->addWidget(inputField);
    inputLayout->addWidget(sendButton);

    // Status
    statusLabel = new QLabel("Ready", this);
    statusLabel->setStyleSheet("color: #E0E0E0; font-size: 11px;");

    // Combine all
    mainLayout->addLayout(headerLayout);
    mainLayout->addWidget(messagesWidget, 1);
    mainLayout->addLayout(inputLayout);
    mainLayout->addWidget(statusLabel);

    centralWidget->setLayout(mainLayout);
}

void MainWindow::setupConnections()
{
    connect(sendButton, &QPushButton::clicked, this, &MainWindow::onSendMessage);
    connect(clearButton, &QPushButton::clicked, this, &MainWindow::onClearHistory);
    connect(apiKeyButton, &QPushButton::clicked, this, &MainWindow::onSetApiKey);
    connect(aiService, &AIService::responseReady, this, &MainWindow::onAiResponse);
    connect(aiService, &AIService::errorOccurred, this, &MainWindow::onAiError);
}

void MainWindow::applyDarkTheme()
{
    QPalette darkPalette;
    darkPalette.setColor(QPalette::Window, QColor("#000000"));
    darkPalette.setColor(QPalette::WindowText, QColor("#ffffff"));
    darkPalette.setColor(QPalette::Base, QColor("#1a1a1a"));
    darkPalette.setColor(QPalette::AlternateBase, QColor("#222222"));
    darkPalette.setColor(QPalette::ToolTipBase, QColor("#000000"));
    darkPalette.setColor(QPalette::ToolTipText, QColor("#ffffff"));
    darkPalette.setColor(QPalette::Text, QColor("#ffffff"));
    darkPalette.setColor(QPalette::Button, QColor("#1a1a1a"));
    darkPalette.setColor(QPalette::ButtonText, QColor("#ffffff"));
    darkPalette.setColor(QPalette::BrightText, QColor("#ffffff"));
    darkPalette.setColor(QPalette::Link, QColor("#569CD6"));
    darkPalette.setColor(QPalette::Highlight, QColor("#333333"));
    darkPalette.setColor(QPalette::HighlightedText, QColor("#ffffff"));

    qApp->setPalette(darkPalette);

    sendButton->setStyleSheet(
        "QPushButton { background-color: #333333; color: #ffffff; border: none; border-radius: 5px; font-weight: bold; }"
        "QPushButton:hover { background-color: #444444; }"
        "QPushButton:pressed { background-color: #222222; }"
        "QPushButton:disabled { opacity: 0.5; }"
    );

    clearButton->setStyleSheet(
        "QPushButton { background-color: #333333; color: #ffffff; border: none; border-radius: 5px; font-weight: bold; }"
        "QPushButton:hover { background-color: #444444; }"
    );

    apiKeyButton->setStyleSheet(
        "QPushButton { background-color: #333333; color: #ffffff; border: none; border-radius: 5px; font-weight: bold; }"
        "QPushButton:hover { background-color: #444444; }"
    );
}

void MainWindow::loadHistory()
{
    auto messages = storageService->loadHistory();
    for (const auto &msg : messages) {
        addMessageToUI(msg.sender, msg.text, msg.sender == "user");
    }
}

void MainWindow::addMessageToUI(const QString &sender, const QString &text, bool isUser)
{
    QListWidgetItem *item = new QListWidgetItem(messagesWidget);

    QString htmlText = QString(
        "<div style='margin: 8px; padding: 10px; border-radius: 8px; background-color: %1;'>"
        "<b style='color: %2;'>%3</b><br>"
        "<span style='color: %4; word-wrap: break-word;'>%5</span><br>"
        "<span style='color: #666666; font-size: 10px; margin-top: 5px;'>%6</span>"
        "</div>"
    )
        .arg(isUser ? "#1a1a1a" : "#222222")
        .arg(isUser ? "#FFFFFF" : "#E0E0E0")
        .arg(sender)
        .arg(isUser ? "#FFFFFF" : "#E0E0E0")
        .arg(text.replace("\n", "<br>"))
        .arg(QTime::currentTime().toString("hh:mm"));

    item->setText(htmlText);
    item->setFlags(item->flags() & ~Qt::ItemIsSelectable);
    messagesWidget->addItem(item);
    messagesWidget->scrollToBottom();

    messageCount++;
}

void MainWindow::onSendMessage()
{
    QString message = inputField->text().trimmed();
    if (message.isEmpty()) return;

    if (!apiKeySet) {
        QMessageBox::warning(this, "API Key Required", "Please set your Gemini API key first");
        onSetApiKey();
        return;
    }

    addMessageToUI("You", message, true);
    inputField->clear();
    sendButton->setEnabled(false);
    statusLabel->setText("Thinking...");

    storageService->saveMessage({"user", message});
    aiService->sendMessage(message, apiKey);
}

void MainWindow::onReturnPressed()
{
    onSendMessage();
}

void MainWindow::onAiResponse(const QString &response)
{
    addMessageToUI("NextAI", response, false);
    storageService->saveMessage({"ai", response});
    sendButton->setEnabled(true);
    statusLabel->setText("Ready");
}

void MainWindow::onAiError(const QString &error)
{
    addMessageToUI("NextAI", "Error: " + error, false);
    sendButton->setEnabled(true);
    statusLabel->setText("Error occurred");
}

void MainWindow::onSetApiKey()
{
    bool ok;
    QString key = QInputDialog::getText(this, "Gemini API Key", "Enter your API key:",
                                       QLineEdit::Password, "", &ok);
    if (ok && !key.isEmpty()) {
        apiKey = key;
        apiKeySet = true;
        statusLabel->setText("API Key set ✓");
        apiKeyButton->setStyleSheet(
            "QPushButton { background-color: #2d5016; color: #ffffff; border: none; border-radius: 5px; font-weight: bold; }"
        );
    }
}

void MainWindow::onClearHistory()
{
    QMessageBox::StandardButton reply = QMessageBox::question(this, "Clear History",
                                                              "Are you sure you want to delete all messages?",
                                                              QMessageBox::Yes | QMessageBox::No);
    if (reply == QMessageBox::Yes) {
        messagesWidget->clear();
        storageService->clearHistory();
        messageCount = 0;
        statusLabel->setText("History cleared");
    }
}
