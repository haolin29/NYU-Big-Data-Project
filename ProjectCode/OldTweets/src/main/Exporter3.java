package main;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.List;

import manager.TweetManager;
import manager.TwitterCriteria;
import model.Tweet;

public class Exporter3 {
	public static void main(String[] args){
		final SimpleDateFormat sdf = new SimpleDateFormat("yyyy/MM/dd HH:mm");
		try {
			for(int i=1; i<31; i+=1) {
				int j = i+1;
				String since = i>9?"2016-04-"+i:"2016-04-0"+i;
				String until = j>9?"2016-04-"+j:"2016-04-0"+j;
				
				System.out.printf("Search on 2016/04/%d%n", i);
				System.out.printf("Current time %s%n", new Timestamp(Calendar.getInstance().getTimeInMillis()));
				TwitterCriteria cr = TwitterCriteria.create()
						.setQuerySearch("donald trump")
						.setSince(since)
						.setUntil(until);
				List<Tweet> tweets = TweetManager.getTweets(cr);
				BufferedWriter bw = new BufferedWriter(new FileWriter(String.format("Trump/April/output_March%d.csv", i)));
				bw.write("username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink");
				for (Tweet t : tweets) {
					bw.newLine();
					bw.write(String.format("%s;%s;%d;%d;\"%s\";%s;%s;%s;\"%s\";%s", t.getUsername(), sdf.format(t.getDate()), t.getRetweets(), t.getFavorites(), t.getText(), t.getGeo(), t.getMentions(), t.getHashtags(), t.getId(), t.getPermalink()));
				}
				bw.close();
				System.out.printf("Successully generated output_trump%d.csv%n", i);
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}