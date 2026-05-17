#ifndef CODEBLOCK_H
#define CODEBLOCK_H

#include <QWidget>
#include <QString>

class CodeBlock : public QWidget
{
    Q_OBJECT

public:
    explicit CodeBlock(const QString &code, const QString &language = "text", QWidget *parent = nullptr);
    ~CodeBlock();

    void paintEvent(QPaintEvent *event) override;
    void mouseDoubleClickEvent(QMouseEvent *event) override;

private:
    QString highlightSyntax(const QString &code);
    void copyToClipboard();

    QString code;
    QString language;
    int lineCount;
};

#endif // CODEBLOCK_H
