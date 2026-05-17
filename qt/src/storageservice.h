#ifndef STORAGESERVICE_H
#define STORAGESERVICE_H

#include <QObject>
#include <QString>
#include <QVector>

struct StoredMessage {
    QString sender;  // "user" or "ai"
    QString text;
    QString timestamp;
};

class StorageService : public QObject
{
    Q_OBJECT

public:
    explicit StorageService(QObject *parent = nullptr);
    ~StorageService();

    void saveMessage(const StoredMessage &message);
    QVector<StoredMessage> loadHistory();
    void clearHistory();

private:
    QString getStoragePath();
    void initializeDatabase();

    QString dbPath;
};

#endif // STORAGESERVICE_H
