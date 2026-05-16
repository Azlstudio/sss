using System;
using System.Collections.Generic;

namespace GTASALauncher
{
    public class ServerData
    {
        public uint ServerId { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public string IP { get; set; }
        public ushort Port { get; set; }
        public string Owner { get; set; }

        // Server Info
        public int MaxPlayers { get; set; }
        public int CurrentPlayers { get; set; }
        public string[] Tags { get; set; }
        public string GameMode { get; set; }

        // Visual
        public string BannerUrl { get; set; }
        public string LogoUrl { get; set; }
        public string IconUrl { get; set; }

        // Meta
        public int PingMs { get; set; }
        public DateTime CreatedDate { get; set; }
        public DateTime LastPlayedDate { get; set; }
        public bool IsFavorite { get; set; }
        public bool IsOnline { get; set; }
        public double Rating { get; set; }
        public int RatingCount { get; set; }

        public string GetPlayersText => $"{CurrentPlayers}/{MaxPlayers}";

        public string GetTagsText => string.Join(", ", Tags ?? Array.Empty<string>());

        public ServerData()
        {
            Tags = new string[] { };
            CreatedDate = DateTime.Now;
            IsOnline = true;
            Rating = 4.5;
            RatingCount = 0;
        }
    }

    public class UserSettings
    {
        public string Username { get; set; }
        public string AccountId { get; set; }
        public List<uint> FavoriteServers { get; set; } = new List<uint>();
        public List<uint> RecentServers { get; set; } = new List<uint>();
        public string Theme { get; set; } = "Dark";
        public bool AutoConnect { get; set; }
        public int MaxServerListSize { get; set; } = 50;
        public string Language { get; set; } = "ES";
        public bool EnableNotifications { get; set; } = true;
        public bool EnableSounds { get; set; } = true;
        public int MasterVolume { get; set; } = 100;
    }

    public class ServerFilter
    {
        public string SearchText { get; set; }
        public string GameMode { get; set; }
        public string[] Tags { get; set; }
        public int MinPlayers { get; set; }
        public int MaxPlayers { get; set; }
        public bool OnlyFavorites { get; set; }
        public bool OnlyOnline { get; set; }
        public string SortBy { get; set; } = "Players"; // Players, Ping, Rating, Name
        public bool SortAscending { get; set; }
    }
}
