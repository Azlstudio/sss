#ifndef AISERVICE_H
#define AISERVICE_H

#include <QObject>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QList>

struct Message {
    QString sender;  // "user" or "ai"
    QString text;
};

class AIService : public QObject
{
    Q_OBJECT

public:
    explicit AIService(QObject *parent = nullptr);
    ~AIService();

    void sendMessage(const QString &message, const QString &apiKey);

signals:
    void responseReady(const QString &response);
    void errorOccurred(const QString &error);

private slots:
    void onNetworkReply();

private:
    QString buildPrompt(const QString &message, const QString &apiKey);
    QString extractCodeBlocks(const QString &text);

    QNetworkAccessManager *networkManager;
    QList<Message> messageHistory;

    static const QString SYSTEM_PROMPT;
    static const int MAX_CONTEXT_MESSAGES;
};

#endif // AISERVICE_H
