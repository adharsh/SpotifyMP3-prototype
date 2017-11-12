import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.List;
import java.util.ArrayList;

public class ParseTextFromURL 
{
	private static String numbers = "1234567890";
	private static String lowercaseLetters = "qwertyuioplkjhgfdsazxcvbnm";
	private static String uppercaseLetters = "QWERTYUIOPLKJHGFDSAZXCVBNM";
	
	public static void main(String[] args) throws IOException, FileNotFoundException
	{
		URL url = new URL("https://open.spotify.com/user/sciencelord01/playlist/3cdIRRtPblsiLVUr4rubOp");

		URLConnection con = url.openConnection();
	    InputStream is =con.getInputStream();

	    BufferedReader br = new BufferedReader(new InputStreamReader(is));

	    String line = null;
	    String html = "";

	    while ((line = br.readLine()) != null) 
	    		html += line + "\n";
	        
		Document doc = Jsoup.parse(html); 
		String text = doc.body().text();
		String[] t = text.split(" ");
		
		List<Integer> indexes = new ArrayList<Integer>();
		for(int x = 0; x < t.length; x++)
		{
			if(t[x].contains("."))
			{
				indexes.add(x);
			}
		}
		
		t = keepIndexes(t, indexes.get(2), indexes.get(indexes.size() - 4));
		
		String[] songInfo = new String[indexes.size() - 6];
		int index = 0;
		for(int x = 0; x < t.length; x++)
		{
			if((numbers.contains(t[x].substring(0, 1))) && (t[x].substring(t[x].length() - 1).equals(".")))
			{
				index++;
			}
			
			if(songInfo[index] == null)
			{
				songInfo[index] = t[x] + " ";
			}
			
			else
			{
				songInfo[index] += t[x] + " ";
			}
		}
		
		songInfo = removeIfNull(songInfo);
		String songinfo = "";
		
		for(int x = 0; x < songInfo.length; x++)
		{
			songInfo[x] = removeAfterChar(songInfo[x], '•');
			songInfo[x] = separateTitleAndArtist(songInfo[x]);
			songInfo[x] = removeNumbers(songInfo[x]);
			songinfo += songInfo[x] + "\n";
		}   
		
		BufferedWriter output = null;
		File file = new File("tmpTitles.txt");
		output = new BufferedWriter(new FileWriter(file));
		output.write(songinfo);
		
		output.close();
	}
	
	private static String[] keepIndexes(String[] t, int lowerBound, int upperBound)
	{
		List<String> kept = new ArrayList<String>();
		for(int x = lowerBound; x <= upperBound; x++)
		{
			kept.add(t[x]);
		}
		
		String[] temp = new String[kept.size()];
		for(int x = 0; x < temp.length; x++)
		{
			temp[x] = kept.get(x);
		}
		
		return temp;
	}
	
	private static String separateTitleAndArtist(String string)
	{
		String temp = "";
		boolean fuckFuck = false;
		for(int x = 0; x < string.length() - 1; x++)
		{
			if(lowercaseLetters.contains(string.substring(x, x + 1)) && uppercaseLetters.contains(string.substring(x + 1, x + 2)))
			{
				temp = string.substring(0, x + 1) + " " + string.substring(x + 1);
				fuckFuck = true;
				break;
			}
		}
		
		return fuckFuck ? temp : string;
	}
	
	private static String removeAfterChar(String string, char remove)
	{
		int index = string.indexOf(remove);
		String temp = "";
		for(int x = 0; x < index; x++)
		{
			temp += string.substring(x, x + 1);
		}
		
		return temp;
	}
	
	private static String[] removeIfNull(String[] t)
	{
		List<String> notNull = new ArrayList<String>();
		for(int x = 0; x < t.length; x++)
		{
			if(t[x] != null)
			{
				notNull.add(t[x]);
			}
		}
		
		String[] temp = new String[notNull.size()];
		for(int x = 0; x < temp.length; x++)
		{
			temp[x] = notNull.get(x);
		}
		
		t = temp;
		return t;
	}
	
	private static String removeNumbers(String s)
	{
		String temp = "";
		
		int index = 0;
		for(int x = 0; x < s.length(); x++)
		{
			if(lowercaseLetters.contains(s.substring(x, x + 1)) || uppercaseLetters.contains(s.substring(x, x + 1)))
			{
				index = x;
				break;
			}
		}
		
		temp = s.substring(index);
		return temp;
	}
}