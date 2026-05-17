#include "storageservice.h"
#include <QStandardPaths>
#include <QSqlDatabase>
#include <QSqlQuery>
#include <QSqlError>
#include <QFile>
#include <QDir>
#include <QDebug>
#include <QDateTime>

StorageService::StorageService(QObject *parent)
    : QObject(parent)
{
    dbPath = getStoragePath();
    initializeDatabase();
}

StorageService::~StorageService()
{
}

QString StorageService::getStoragePath()
{
    QString dataPath = QStandardPaths::writableLocation(QStandardPaths::AppLocalDataLocation);
    QDir().mkpath(dataPath);
    return dataPath + "/nextai.db";
}

void StorageService::initializeDatabase()
{
    QSqlDatabase db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName(dbPath);

    if (!db.open()) {
        qWarning() << "Failed to open database:" << db.lastError().text();
        return;
    }

    QSqlQuery query;
    query.exec("CREATE TABLE IF NOT EXISTS messages ("
              "id INTEGER PRIMARY KEY AUTOINCREMENT,"
              "sender TEXT NOT NULL,"
              "text TEXT NOT NULL,"
              "timestamp DATETIME DEFAULT CURRENT_TIMESTAMP"
              ")");

    if (query.lastError().isValid()) {
        qWarning() << "Failed to create table:" << query.lastError().text();
    }
}

void StorageService::saveMessage(const StoredMessage &message)
{
    QSqlDatabase db = QSqlDatabase::database();
    if (!db.isOpen()) {
        qWarning() << "Database is not open";
        return;
    }

    QSqlQuery query;
    query.prepare("INSERT INTO messages (sender, text, timestamp) VALUES (?, ?, ?)");
    query.addBindValue(message.sender);
    query.addBindValue(message.text);
    query.addBindValue(QDateTime::currentDateTime().toString(Qt::ISODate));

    if (!query.exec()) {
        qWarning() << "Failed to save message:" << query.lastError().text();
    }
}

QVector<StoredMessage> StorageService::loadHistory()
{
    QVector<StoredMessage> messages;
    QSqlDatabase db = QSqlDatabase::database();

    if (!db.isOpen()) {
        qWarning() << "Database is not open";
        return messages;
    }

    QSqlQuery query("SELECT sender, text, timestamp FROM messages ORDER BY timestamp ASC");

    while (query.next()) {
        StoredMessage msg;
        msg.sender = query.value(0).toString();
        msg.text = query.value(1).toString();
        msg.timestamp = query.value(2).toString();
        messages.append(msg);
    }

    return messages;
}

void StorageService::clearHistory()
{
    QSqlDatabase db = QSqlDatabase::database();
    if (!db.isOpen()) {
        qWarning() << "Database is not open";
        return;
    }

    QSqlQuery query("DELETE FROM messages");
    if (!query.exec()) {
        qWarning() << "Failed to clear history:" << query.lastError().text();
    }
}
