#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QListWidget>
#include <QLineEdit>
#include <QPushButton>
#include <QLabel>
#include "aiservice.h"
#include "storageservice.h"

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void onSendMessage();
    void onClearHistory();
    void onSetApiKey();
    void onAiResponse(const QString &response);
    void onAiError(const QString &error);
    void onReturnPressed();

private:
    void setupUI();
    void setupConnections();
    void loadHistory();
    void addMessageToUI(const QString &sender, const QString &text, bool isUser);
    void applyDarkTheme();

    // UI Components
    QListWidget *messagesWidget;
    QLineEdit *inputField;
    QPushButton *sendButton;
    QPushButton *clearButton;
    QPushButton *apiKeyButton;
    QLabel *titleLabel;
    QLabel *statusLabel;

    // Services
    AIService *aiService;
    StorageService *storageService;

    // State
    QString apiKey;
    bool apiKeySet;
    int messageCount;
};

#endif // MAINWINDOW_H
